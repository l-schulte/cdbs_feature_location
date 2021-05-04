import math
import os
from typing import List, Tuple
from data import data


def train(mdl, documents: List[data.Document], features, path, file_prefix='') \
        -> Tuple[List[dict], object, bool]:

    data_list = []
    mdl.burn_in = 10

    for document in documents:

        word_list = document.get_word_list(features)

        if word_list:
            idx = mdl.add_doc(word_list)
            tmp = {
                'id': str(document._id),
                'features': list(document.feature_ids),
                'name': document.name,
                'path': document.path,
                'model_index': idx
            }
            data_list.append(tmp)

    if not os.path.exists('{}/tmp'.format(path)):
        os.mkdir('{}/tmp'.format(path))

    iterations = 1000
    steps = 10
    retrys = 0
    max_retrys = 2
    i = 0
    while i < iterations:
        mdl.train(steps)
        i += steps

        if math.isnan(mdl.ll_per_word) and retrys < max_retrys:
            mdl = mdl.load('{}/tmp/{}_i{}.mdl'.format(path, file_prefix, i))
            retrys += 1
            print('v Iteration: {}\t Retry: {}/{}'.format(i, retrys, max_retrys))
            continue

        if retrys == max_retrys:
            return data_list, mdl, False

        retrys = 0
        print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

        mdl.save('{}/tmp/{}_i{}.mdl'.format(path, file_prefix, i))

    mdl.save('{}/{}.mdl'.format(path, file_prefix))
    print('PA ll per word  \t{}'.format(mdl.ll_per_word))
    return data_list, mdl, True
