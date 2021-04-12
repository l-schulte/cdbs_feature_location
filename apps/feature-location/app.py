import argparse
import os
import progressbar
import json
import math
from models import lda, pachinko
from data import data, get_db_features
from validation import mean_reciprocal_rank as MRR


def evaluate(args):

    queries = []
    filenames = []

    if args.input:
        path = '{}\\queries\\'.format(args.input)
        filenames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        for filename in filenames:
            f = open('{}{}'.format(path, filename), 'r')
            queries.append(f.read())
            f.close()

    elif args.query:
        filenames.append('x')
        queries.append(args.query)

    def save_or_print(path, res):
        if args.input:
            f = open(path, 'w')
            f.write(res)
            f.close()
        else:
            print(res)

    for filename, query in progressbar.progressbar(zip(filenames, queries)):

        if 'lda' in args.eval:
            tmp = lda.evaluate(query, args.lda_k1)
            res_lda = lda.interpret(tmp, args.pages, args.classes, args.methods, args.determination, args.lda_k1)
            save_or_print('{}\\queries\\{}\\{}'.format(args.input, 'lda', filename), res_lda)

        if 'pa' in args.eval:
            tmp = pachinko.evaluate(query, args.pa_k1, args.pa_k2)
            res_pa = pachinko.interpret(tmp, args.pages, args.classes, args.methods,
                                        args.determination, args.pa_k1, args.pa_k2)
            save_or_print('{}\\queries\\{}\\{}'.format(args.input, 'pa', filename), res_pa)


def train(args):

    documents = data.get_documents(args.base)

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

    if 'lda' in args.train:
        result.append(lda.train(documents, features, args.lda_k1))

    if 'pa' in args.train:
        result.append(pachinko.train(documents, features, args.pa_k1, args.pa_k2))

    return result


def validate(args):

    goldsets_path = '{}\\goldsets\\class\\'.format(args.input)
    queries_path = '{}\\queries\\'.format(args.input)

    goldsets = data.read_goldsets(goldsets_path)

    result = {}

    if 'lda' in args.validate:
        results_lda = data.read_query_results('{}lda\\'.format(queries_path))
        mrr_lda = MRR.calculate(goldsets, results_lda)

        print('LDA MRR: \t{}'.format(mrr_lda))
        result['lda'] = mrr_lda

    if 'pa' in args.validate:
        results_pa = data.read_query_results('{}pa\\'.format(queries_path))
        mrr_pa = MRR.calculate(goldsets, results_pa)

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

        # - eval
        parser.add_argument('-e', '--eval', nargs='+', choices=['lda', 'pa'], help='evaluate cluster')
        parser.add_argument('-q', '--query', help='evaluate text query, will be ignored if input dir is chosen')
        parser.add_argument('-i', '--input', help='directory with text files interpretet as input')
        parser.add_argument('-m', '--methods', action='store_true', help='list methods')
        parser.add_argument('-c', '--classes', action='store_true', help='list classes')
        parser.add_argument('-p', '--pages', help='number of documents', default=1000, type=int)
        parser.add_argument('-d', '--determination', choices=['ml', 'dist'],
                            help='method of determination which documents are simmilar', default='dist')

        # - validate
        parser.add_argument('-v', '--validate', nargs='+', choices=['lda', 'pa'], help='validate cluster')

        # - general
        parser.add_argument('--json', action='store_true', help='returns output as JSON document')

        args = parser.parse_args()

    result = {}

    if args.train:
        print('--- train ------')
        result['train'] = train(args)

    if args.eval:
        print('--- evaluate ---')
        result['evaluate'] = evaluate(args)

    if args.validate:
        print('--- validate ---')
        result['validate'] = validate(args)

    return result


def optimize_training():

    dump_path = 'optimize_dump.json'
    if os.path.isfile(dump_path):
        results = json.load(open(dump_path, 'r'))
    else:
        results = {}

    args = type('', (), {})()
    args.train = 'pa'
    args.eval = None
    args.validate = None
    args.base = 'class'

    for k1 in range(10, 400, 50):
        args.pa_k1 = k1
        for k2 in range(10, 400, 50):
            args.pa_k2 = k2

            result_id = 'k1_{}_k2_{}'.format(k1, k2)
            print('k1: {} \t k2: \t{}'.format(k1, k2))

            if result_id in results and not math.isnan(results[result_id]['result']['train'][0][args.train]):
                print('skip, ll = \t{}'.format(results[result_id]['result']['train'][0][args.train]))
                continue

            res = execute(args)
            results[result_id] = {'k1': k1, 'k2': k2, 'result': res}

            json.dump(results, open('optimize_dump.json', 'w'), indent=4)


if __name__ == "__main__":
    # execute()
    optimize_training()
