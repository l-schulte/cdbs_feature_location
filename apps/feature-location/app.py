import argparse
import os
import progressbar
from models import lda, pachinko


def eval(parser, args):

    print(args.pages)

    queries = []
    filenames = []

    if args.input:
        filenames = [f for f in os.listdir(args.input) if os.path.isfile(os.path.join(args.input, f))]
        print('\n'.join(filenames))

        for filename in filenames:
            f = open('{}{}'.format(args.input, filename), 'r')
            queries.append(f.read())
            f.close()

    elif args.query:
        filenames.append('x')
        queries.append(args.query)

    def save_or_print(path, type, res):
        if args.input:
            f = open('{}.result.{}.txt'.format(path, type), 'w')
            f.write(res)
            f.close()
        else:
            print(res)

    for filename, query in progressbar.progressbar(zip(filenames, queries)):

        if 'lda' in args.eval:
            tmp = lda.evaluate(query)
            res = lda.interpret(tmp, args.pages, args.classes, args.methods, args.json)
            save_or_print('{}{}'.format(args.input, filename), 'lda', res)

        if 'pa' in args.eval:
            tmp = pachinko.evaluate(query)
            res = pachinko.interpret(tmp, args.pages, args.classes, args.methods, args.json)
            save_or_print('{}{}'.format(args.input, filename), 'pa', res)


def train(parser, args):
    if 'lda' in args.train:
        lda.train()

    if 'pa' in args.train:
        pachinko.train()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train', nargs='+', choices=['lda', 'pa'], help='train cluster')
    parser.add_argument('-e', '--eval', nargs='+', choices=['lda', 'pa'], help='evaluate cluster')
    parser.add_argument('-q', '--query', help='evaluate text query, will be ignored if input dir is chosen')
    parser.add_argument('-i', '--input', help='directory with text files interpretet as input')
    parser.add_argument('-m', '--methods', action='store_true', help='list methods')
    parser.add_argument('-c', '--classes', action='store_true', help='list classes')
    parser.add_argument('-p', '--pages', help='number of documents', default=10, type=int)
    parser.add_argument('--json', action='store_true', help='returns output as JSON document')

    args = parser.parse_args()

    if args.train:
        train(parser, args)

    if args.eval:
        eval(parser, args)


main()
