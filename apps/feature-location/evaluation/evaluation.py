from data import data
import os

from evaluation import tomotopy


def get_queries_and_filenames(input_path=None, query=None):
    queries = []
    filenames = []

    if input_path:
        path = '{}\\queries\\'.format(input_path)
        filenames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        for filename in filenames:
            f = open('{}{}'.format(path, filename), 'r')
            queries.append(f.read())
            f.close()

    elif query:
        filenames.append('x')
        queries.append(query)

    return queries, filenames


def evaluate(mdl, text: str):
    word_list = data.nltk_filter(text)
    return tomotopy.evaluate(mdl, word_list)


def save_or_print(args, path, file, res):
    if not os.path.exists(path):
        os.mkdir(path)
    if args.input:
        f = open('{}/{}'.format(path, file), 'w')
        f.write(res)
        f.close()
    else:
        print(res)
