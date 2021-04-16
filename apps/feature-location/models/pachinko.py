from models.models import get_json, tomotopy_train
import tomotopy as tp
import pandas as pd
import json
from data import data

FILE_NAME = 'pa'


def interpret(results, path, top_n, classes, methods, determination, k1, k2):

    (super_topics_prob, sub_topics_prob), log_ll = results

    if k1 and k2:
        df = pd.read_csv('{}/{}_{}_{}.csv'.format(path, FILE_NAME, k1, k2))
    else:
        df = pd.read_csv('{}/{}.csv'.format(path, FILE_NAME))

    if determination == 'ml':

        max_value_super = max(super_topics_prob)
        max_index_super = super_topics_prob.tolist().index(max_value_super)

        max_value_sub = max(sub_topics_prob)
        max_index_sub = sub_topics_prob.tolist().index(max_value_sub)

        df['most_likely'] = (df['topic_{}'.format(max_index_super)] + df['sub_topic_{}'.format(max_index_sub)]) / 2

    elif determination == 'dist':

        df['most_likely_super'] = sum([abs(df['topic_{}'.format(i)] - ri)
                                       for i, ri in enumerate(super_topics_prob)]) / len(super_topics_prob)

        df['most_likely_sub'] = sum([abs(df['sub_topic_{}'.format(i)] - ri)
                                     for i, ri in enumerate(sub_topics_prob)]) / len(sub_topics_prob)

        df['most_likely'] = abs(df.most_likely_super - df.most_likely_sub) / 2
        # df['most_likely'] = df['most_likely_sub']

    else:
        raise Exception('missing determination method by parameter -d --determination = ml or dist')

    sorted_df = df.sort_values(by='most_likely', ascending=False)

    return get_json(sorted_df, log_ll, top_n, classes, methods)


def evaluate(text, path, k1, k2):

    word_list = data.nltk_filter(text)
    # print('\nevaluating <{}> for pa...'.format(text))
    # print('\nword list contains {} words <{}>'.format(len(word_list), ' '.join(word_list)))

    if k1 and k2:
        mdl = tp.PAModel().load('{}/{}_{}_{}.mdl'.format(path, FILE_NAME, k1, k2))
    else:
        mdl = tp.PAModel().load('{}/{}.mdl'.format(path, FILE_NAME))

    if word_list:
        doc = mdl.make_doc(word_list)

        return mdl.infer(doc)

    return 'error'


def train(documents, features, path, topic_n_k1=20, topics_n_k2=20):

    file_prefix = '{}/{}_{}_{}'.format(path, FILE_NAME, topic_n_k1, topics_n_k2)

    success = False
    retrys = 0
    max_retrys = 10

    while not success and retrys < max_retrys:

        mdl = tp.PAModel(k1=topic_n_k1, k2=topics_n_k2, rm_top=20)
        data_list, mdl, success = tomotopy_train(mdl, documents, features, file_prefix)

    for row in data_list:

        doc = mdl.docs[row['model_index']]
        topics = doc.get_topics(top_n=topic_n_k1)
        topics = sorted(topics, key=lambda item: item[0])

        for t in range(topic_n_k1):
            row['topic_{}'.format(t)] = topics[t][1]

        sub_topics = doc.get_sub_topics(top_n=topics_n_k2)
        sub_topics = sorted(sub_topics, key=lambda item: item[0])

        for t in range(topics_n_k2):
            row['sub_topic_{}'.format(t)] = sub_topics[t][1]

    columns = list(data_list[0].keys())
    mapping = pd.DataFrame(data_list, columns=columns)

    # print(res)

    json.dump(data_list, open(file_prefix + '.json', 'w'), indent=4)
    mapping.to_csv(file_prefix + '.csv')

    return {FILE_NAME: mdl.ll_per_word}
