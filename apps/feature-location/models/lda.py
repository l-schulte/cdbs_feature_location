from models.models import get_page, get_json
import tomotopy as tp
import pandas as pd
import json

from data import data

FILE_NAME = 'lda'


def interpret(results, top_n=10, classes=False, methods=False, json=False):

    result, log_ll = results
    max_value = max(result)
    max_index = result.tolist().index(max_value)

    df = pd.read_csv('{}.csv'.format(FILE_NAME))

    sorted_df = df.sort_values(by='topic_{}'.format(max_index))

    if json:
        return get_json(sorted_df, log_ll, top_n, classes, methods)

    print('log_ll = {}'.format(log_ll))
    return get_page(sorted_df, top_n, classes, methods)


def evaluate(text):

    word_list = data.nltk_filter(text)

    # print('\nevaluating <{}> for lda...'.format(text))
    # print('\nword list contains {} words <{}>'.format(len(word_list), ' '.join(word_list)))

    mdl = tp.LDAModel().load('{}.mdl'.format(FILE_NAME))

    if word_list:
        doc = mdl.make_doc(word_list)

        return mdl.infer(doc)

    return 'error'


def train(topic_n=20):

    db_commits = data.get_db()
    mdl = tp.LDAModel(k=topic_n, seed=123)

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
        # print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

    # for k in range(mdl.k):
    #     print('Top 10 words of topic #{}'.format(k))
    #     print(mdl.get_topic_words(k, top_n=3))

    # mdl.summary()

    for row in data_list:

        doc = mdl.docs[row['model_index']]
        topics = doc.get_topics(top_n=topic_n)
        topics = sorted(topics, key=lambda item: item[0])

        for t in range(topic_n):
            row['topic_{}'.format(t)] = topics[t][1]

    columns = ['id', 'feature', 'mapping', 'model_index']
    columns.extend(['topic_{}'.format(t) for t in range(topic_n)])
    mapping = pd.DataFrame(data_list, columns=columns)

    # print(res)

    mdl.save('{}.mdl'.format(FILE_NAME))

    print('LDA ll per word \t{}'.format(mdl.ll_per_word))

    mapping.to_csv('{}.csv'.format(FILE_NAME))
