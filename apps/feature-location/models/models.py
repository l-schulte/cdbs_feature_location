import json
from typing import List
from data import data


def __get_word_list(features, document: data.Document):
    word_list = []

    for feature_id in document.feature_ids:
        if feature_id in features:
            word_list.extend(features[feature_id]['words'])

    return word_list


def tomotopy_train(mdl, documents: List[data.Document], features) -> List[dict]:

    data_list = []
    mdl.burn_in = 10

    # export = []

    for document in documents:

        word_list = __get_word_list(features, document)

        if word_list:
            idx = mdl.add_doc(word_list)
            tmp = {
                'id': document._id,
                'features': document.feature_ids,
                'name': document.name,
                'path': document.path,
                'model_index': idx
            }
            data_list.append(tmp)
            # export.append(word_list)

    # json.dump(export, open('export.json', 'w'))
    # exit()

    mdl.train(1000)
    # print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

    # if hasattr(mdl, 'k'):
    #     k = mdl.k
    # if hasattr(mdl, 'k2'):
    #     k = mdl.k2

    # for k in range(k):
    #     print('Top 5 words of topic #{}'.format(k))
    #     print(mdl.get_topic_words(k, top_n=5))

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

    for id, path, name in zip(df.id[0:top_n], df.path[0:top_n], df.name[0:top_n]):
        res['res'].append({'_id': id, 'path': path, 'name': name})

    return json.dumps(res, indent=4, sort_keys=False)
