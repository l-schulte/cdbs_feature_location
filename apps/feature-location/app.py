import argparse
import os
import progressbar
from models import lda, pachinko
from data import data, get_db_features, get_db_files
from validation import mean_reciprocal_rank as MRR


def eval(args):

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
            tmp = lda.evaluate(query)
            res_lda = lda.interpret(tmp, args.pages, args.classes, args.methods, args.json)
            save_or_print('{}\\queries\\{}\\{}'.format(args.input, 'lda', filename), res_lda)

        if 'pa' in args.eval:
            tmp = pachinko.evaluate(query)
            res_pa = pachinko.interpret(tmp, args.pages, args.classes, args.methods, args.json)
            save_or_print('{}\\queries\\{}\\{}'.format(args.input, 'pa', filename), res_pa)


def train(args):

    documents = data.get_documents(args.base)

    print(len(documents))

    features = get_db_features().find_one()
    features = data.nltk_feature_filter(features)

    if 'lda' in args.train:
        lda.train(documents, features, args.lda_k1)

    if 'pa' in args.train:
        pachinko.train(documents, features, args.pa_k1, args.pa_k2)


def validate(args):

    goldsets_path = '{}\\goldsets\\class\\'.format(args.input)
    queries_path = '{}\\queries\\'.format(args.input)

    goldsets = data.read_goldsets(goldsets_path)

    if 'lda' in args.validate:
        results_lda = data.read_query_results('{}lda\\'.format(queries_path))
        mrr_lda = MRR.calculate(goldsets, results_lda)

        print('LDA MRR: \t{}'.format(mrr_lda))

    if 'pa' in args.validate:
        results_pa = data.read_query_results('{}pa\\'.format(queries_path))
        mrr_pa = MRR.calculate(goldsets, results_pa)

        print('PA MRR: \t{}'.format(mrr_pa))


def main():
    parser = argparse.ArgumentParser()

    # - train
    parser.add_argument('-t', '--train', nargs='+', choices=['lda', 'pa'], help='train cluster')
    parser.add_argument('--lda_k1', help='number of topics for lda', default=20, type=int)
    parser.add_argument('--pa_k1', help='number of topics for pa', default=20, type=int)
    parser.add_argument('--pa_k2', help='number of subtopics for pa', default=20, type=int)
    parser.add_argument('-b', '--base', help='file or class based', choices=['file', 'class'], default='file', type=str)

    # - eval
    parser.add_argument('-e', '--eval', nargs='+', choices=['lda', 'pa'], help='evaluate cluster')
    parser.add_argument('-q', '--query', help='evaluate text query, will be ignored if input dir is chosen')
    parser.add_argument('-i', '--input', help='directory with text files interpretet as input')
    parser.add_argument('-m', '--methods', action='store_true', help='list methods')
    parser.add_argument('-c', '--classes', action='store_true', help='list classes')
    parser.add_argument('-p', '--pages', help='number of documents', default=10, type=int)

    # - validate
    parser.add_argument('-v', '--validate', nargs='+', choices=['lda', 'pa'], help='validate cluster')

    # - general
    parser.add_argument('--json', action='store_true', help='returns output as JSON document')

    args = parser.parse_args()

    if args.train:
        print('--- train ------')
        train(args)

    if args.eval:
        print('--- evaluate ---')
        eval(args)

    if args.validate:
        print('--- validate ---')
        validate(args)


main()
