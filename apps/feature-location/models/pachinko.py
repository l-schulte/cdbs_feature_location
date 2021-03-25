from models.models import get_json, get_page
import tomotopy as tp
import pandas as pd
import json

from data import data

FILE_NAME = 'pa'
TOPICS_K1 = 10
TOPICS_K2 = 10


def interpret(results, top_n=10, classes=False, methods=False, json=False):

    (super_topics_prob, sub_topics_prob), log_ll = results

    max_value_super = max(super_topics_prob)
    max_index_super = super_topics_prob.tolist().index(max_value_super)

    max_value_sub = max(sub_topics_prob)
    max_index_sub = sub_topics_prob.tolist().index(max_value_sub)

    df = pd.read_csv('{}.csv'.format(FILE_NAME))

    df['most_likely'] = (df['topic_{}'.format(max_index_super)] + df['topic_{}'.format(max_index_sub)]) / 2
    sorted_df = df.sort_values(by='most_likely')

    if json:
        return get_json(sorted_df, log_ll, top_n, classes, methods)

    print('log_ll = {}'.format(log_ll))
    return get_page(sorted_df, top_n, classes, methods)

    # super_topics = list(enumerate(super_topics_prob, 0))
    # sub_topics = list(enumerate(sub_topics_prob, 0))

    # print(super_topics)
    # print(sub_topics)

    # topic_combinations = []
    # for i, super_topic_prob in super_topics:
    #     for j, sub_topic_prob in sub_topics:
    #         mean = (super_topic_prob + sub_topic_prob) / 2
    #         topic_combinations.append((i, j, mean))

    # topic_combinations = sorted(topic_combinations, key=lambda t: t[2], reverse=True)


def evaluate(text):

    word_list = data.nltk_filter(text)
    # print('\nevaluating <{}> for pa...'.format(text))
    # print('\nword list contains {} words <{}>'.format(len(word_list), ' '.join(word_list)))

    mdl = tp.PAModel().load('{}.mdl'.format(FILE_NAME))

    if word_list:
        doc = mdl.make_doc(word_list)

        return mdl.infer(doc)

    return 'error'


def train():

    db_commits = data.get_db()
    mdl = tp.PAModel(k1=TOPICS_K1, k2=TOPICS_K2, seed=123)

    data_list = []

    for document in db_commits.find(limit=1000):
        word_list = data.nltk_doc_filter(document)
        if word_list:
            idx = mdl.add_doc(word_list)
            tmp = {
                'id': str(document['_id']),
                'feature': document['feature_id'],
                'mapping': json.dumps(document['diff']),
                'model_index': idx
            }
            data_list.append(tmp)

    for i in range(0, 100, 10):
        mdl.train(10)
        print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

    # for k in range(mdl.k2):
    #     print('Top 10 words of topic #{}'.format(k))
    #     print(mdl.get_topic_words(k, top_n=3))

    mdl.summary()

    for row in data_list:

        doc = mdl.docs[row['model_index']]
        topics = doc.get_topics(top_n=TOPICS_K1)
        topics = sorted(topics, key=lambda item: item[0])

        for t in range(TOPICS_K1):
            row['topic_{}'.format(t)] = topics[t][1]

        sub_topics = doc.get_sub_topics(top_n=TOPICS_K2)
        sub_topics = sorted(sub_topics, key=lambda item: item[0])

        for t in range(TOPICS_K2):
            row['sub_topic_{}'.format(t)] = sub_topics[t][1]

    columns = ['id', 'feature', 'mapping', 'model_index']
    columns.extend(['topic_{}'.format(t) for t in range(TOPICS_K1)])
    columns.extend(['sub_topic_{}'.format(t) for t in range(TOPICS_K2)])
    mapping = pd.DataFrame(data_list, columns=columns)

    # print(res)

    mdl.save('{}.mdl'.format(FILE_NAME))

    mapping.to_csv('{}.csv'.format(FILE_NAME))
