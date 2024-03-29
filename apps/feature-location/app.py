import argparse
import os
import progressbar
import json
import time
from datetime import datetime
import math
from models import tp_lda, tp_pachinko
from data import data, get_db_features
from validation import validation
from evaluation import evaluation
from training import training


def __train(args):

    if not os.path.exists(args.input):
        os.mkdir(args.input)

    documents = data.get_documents(args.base)

    print('Documents: {}'.format(len(documents)))

    all_features = get_db_features().find_one()
    features = {}
    for feature_id in all_features:
        if feature_id == '_id':
            continue
        if all_features[feature_id]['type']['name'] not in []:
            features[feature_id] = all_features[feature_id]

    features = data.nltk_feature_filter(features)

    print('skipped {} entries'.format(len(all_features) - len(features)))

    result = []

    max_retrys = 3

    if 'lda' in args.train:
        retrys = 0
        success = False
        while not success and retrys < max_retrys:
            mdl, file_prefix = tp_lda.create_model(args.lda_k1, args.alpha, args.eta)
            data_list, mdl, success = training.train(mdl, documents, features, args.input, file_prefix,
                                                     args.iterations, args.burn_in)
            retrys += 1

        res = tp_lda.save_model(mdl, args.lda_k1, data_list, args.input, file_prefix)
        result.append(res)

    if 'pa' in args.train:
        retrys = 0
        success = False
        while not success and retrys < max_retrys:
            mdl, file_prefix = tp_pachinko.create_model(args.pa_k1, args.pa_k2, args.alpha, args.sub_alpha, args.eta)
            data_list, mdl, success = training.train(mdl, documents, features, args.input, file_prefix,
                                                     args.iterations, args.burn_in)
            retrys += 1

        res = tp_pachinko.save_model(mdl, args.pa_k1, args.pa_k2, data_list, args.input, file_prefix)
        result.append(res)

    return result


def __evaluate(args):

    queries, filenames = evaluation.get_queries_and_filenames(args.input, args.query)

    for filename, query in progressbar.progressbar(zip(filenames, queries)):

        if 'lda' in args.eval:
            modelname = 'lda_{}.mdl'.format(args.lda_k1)
            mdl = tp_lda.load_model(args.input, modelname)
            tmp = evaluation.evaluate(mdl, query)
            res_lda = tp_lda.interpret_evaluation_results(tmp, args.input, args.pages, args.determ, args.lda_k1)
            evaluation.save_or_print(args, '{}queries/{}'.format(args.input, 'lda'), filename, res_lda)

        if 'pa' in args.eval:
            modelname = 'pa_{}_{}.mdl'.format(args.pa_k1, args.pa_k2)
            mdl = tp_pachinko.load_model(args.input, modelname)
            tmp = evaluation.evaluate(mdl, query)
            res_pa = tp_pachinko.interpret_evaluation_results(
                tmp, args.input, args.pages, args.determ, args.pa_k1, args.pa_k2)
            evaluation.save_or_print(args, '{}queries/{}'.format(args.input, 'pa'), filename, res_pa)


def __validate(args):

    goldsets_path = '{}/goldsets/class/'.format(args.input)
    queries_path = '{}/queries/'.format(args.input)

    goldsets = data.read_goldsets(goldsets_path)

    result = {}

    if 'lda' in args.validate:
        results_lda = data.read_query_results('{}lda/'.format(queries_path))
        mrr_lda = validation.get_score(goldsets, results_lda)

        print('LDA MRR: \t{}'.format(mrr_lda))
        result['lda'] = mrr_lda

    if 'pa' in args.validate:
        results_pa = data.read_query_results('{}pa/'.format(queries_path))
        mrr_pa = validation.get_score(goldsets, results_pa)

        print('PA MRR: \t{}'.format(mrr_pa))
        result['pa'] = mrr_pa

    return result


def execute(args=None):

    if not args:
        parser = argparse.ArgumentParser()

        # - train
        parser.add_argument('-t', '--train', nargs='+', choices=['lda', 'pa'], help='train cluster')
        parser.add_argument('--lda_k1', help='number of topics for lda', default=20, type=int)
        parser.add_argument('--pa_k1', help='number of topics for pa', default=20, type=int)
        parser.add_argument('--pa_k2', help='number of subtopics for pa', default=20, type=int)
        parser.add_argument('-b', '--base', help='file or class based',
                            choices=['file', 'class'], default='class', type=str)
        parser.add_argument('--iterations', help='number of training iterations', default=100, type=int)
        parser.add_argument('--burn_in', help='burn in for training', default=10, type=int)
        parser.add_argument('--alpha', help='alpha parameter for training', default=0.1, type=float)
        parser.add_argument('--sub_alpha', help='sub alpha parameter for training of PA', default=0.1, type=float)
        parser.add_argument('--eta', help='eta parameter for training', default=0.1, type=float)

        # - eval
        parser.add_argument('-e', '--eval', nargs='+', choices=['lda', 'pa'], help='evaluate cluster')
        parser.add_argument('-q', '--query', help='evaluate text query, will be ignored if input dir is chosen')
        parser.add_argument('-i', '--input', help='directory with text files interpretet as input')
        parser.add_argument('-p', '--pages', help='number of documents', default=1000, type=int)
        parser.add_argument('-d', '--determ', choices=['ml', 'dist'],
                            help='method of determination which documents are simmilar', default='dist')

        # - validate
        parser.add_argument('-v', '--validate', nargs='+', choices=['lda', 'pa'], help='validate cluster')

        args = parser.parse_args()

    result = {}

    if args.train:
        print('--- train ------')
        result['train'] = __train(args)

    if args.eval:
        print('--- evaluate ---')
        result['evaluate'] = __evaluate(args)

    if args.validate:
        print('--- validate ---')
        result['validate'] = __validate(args)

    return result


def optimize_training():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='directory with text files interpretet as input')
    args = parser.parse_args()

    dir_name = str('optimize_{}'.format(datetime.now().timestamp()).replace('.', ''))
    if args.input:
        dir_name = args.input

    dump_path = '{}/optimize_dump.json'.format(dir_name)

    if os.path.isfile(dump_path):
        results = json.load(open(dump_path, 'r'))
    else:
        results = {}

        os.mkdir(dir_name)

    args = type('', (), {})()
    args.train = 'pa'
    args.input = dir_name
    args.eval = None
    args.validate = None
    args.base = 'class'

    for k1 in range(50, 401, 50):
        args.pa_k1 = k1
        for k2 in range(50, 301, 50):
            args.pa_k2 = k2

            result_id = 'k1_{}_k2_{}'.format(k1, k2)
            print('k1: {} \t k2: \t{}'.format(k1, k2))

            if result_id in results and not math.isnan(results[result_id]['result']['train'][0][args.train]):
                print('skip, ll = \t{}'.format(results[result_id]['result']['train'][0][args.train]))
                continue

            res = execute(args)
            results[result_id] = {'k1': k1, 'k2': k2, 'result': res}

            json.dump(results, open(dump_path, 'w'), indent=4)


if __name__ == "__main__":

    data.get_files()

    def time_convert(sec):
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        print("Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), sec))

    start = time.time()

    execute()
    # optimize_training()

    time_lapsed = time.time() - start
    time_convert(time_lapsed)
