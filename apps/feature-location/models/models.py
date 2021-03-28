import json
from typing import List
from data import data, get_db_features, get_db_files


def __get_word_list(features, file):
    word_list = []

    for feature_id in file['feature_ids']:
        if feature_id in features:
            word_list.extend(features[feature_id])

    return word_list


def tomotopy_train(mdl) -> List[dict]:

    features = get_db_features().find_one()
    features = data.nltk_feature_filter(features)

    data_list = []

    for file in get_db_files().find():

        word_list = __get_word_list(features, file)

        if word_list:
            idx = mdl.add_doc(word_list)
            tmp = {
                'id': str(file['_id']),
                'features': file['feature_ids'],
                'path': file['path'],
                'model_index': idx
            }
            data_list.append(tmp)

    for i in range(0, 100, 10):
        mdl.train(10)
        # print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

    # for k in range(mdl.k2):
    #     print('Top 10 words of topic #{}'.format(k))
    #     print(mdl.get_topic_words(k, top_n=3))

    # mdl.summary()

    return data_list


def get_page(df, top_n, classes, methods):
    res = []
    for cnt, path in enumerate(df.path[0:top_n], 1):

        res.append('- {} -'.format(cnt))

        if len(path) == 0:
            res.append(' x')

        res.append(' {}'.format(path))

    return '\n'.join(res)


def get_json(df, log_ll, top_n, classes, methods):

    res = {'log_ll': log_ll, 'res': []}

    for id, path in zip(df.id[0:top_n], df.path[0:top_n]):
        res['res'].append({'_id': id, 'path': path})

    return json.dumps(res, indent=4)
