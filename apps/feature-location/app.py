import argparse

from models import lda, pachinko


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train', nargs='+', choices=['lda', 'pa'], help='train cluster')
    parser.add_argument('-e', '--eval', nargs='+', choices=['lda', 'pa'], help='evaluate cluster')
    parser.add_argument('-q', '--query', help='evaluate text query')
    parser.add_argument('-f', '--functions', action='store_true', help='list functions')
    parser.add_argument('-n', '--number', help='number of documents')

    args = parser.parse_args()

    if args.train:

        if 'lda' in args.train:
            lda.train()

        if 'pa' in args.train:
            pachinko.train()

    if args.eval:

        if not args.query:
            print("text query ['-q', '--query'] required for evaluation")

        if 'lda' in args.eval:
            res = lda.evaluate(args.query)
            lda.display(res, functions=args.functions)

        if 'pa' in args.eval:
            res = pachinko.evaluate(args.query)
            pachinko.display(res, functions=args.functions)


main()
