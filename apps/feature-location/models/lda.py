from models.models import get_json, tomotopy_train
import tomotopy as tp
import pandas as pd

from data import data

FILE_NAME = 'lda'


def interpret(results, top_n, classes, methods, determination, k1):

    result, log_ll = results
    if k1:
        df = pd.read_csv('{}_{}.csv'.format(FILE_NAME, k1))
    else:
        df = pd.read_csv('{}.csv'.format(FILE_NAME, k1))

    if determination == 'ml':
        max_value = max(result)
        max_index = result.tolist().index(max_value)
        df['most_likely'] = df['topic_{}'.format(max_index)]

    elif determination == 'dist':
        df['most_likely'] = sum([abs(df['topic_{}'.format(i)] - ri) for i, ri in enumerate(result)]) / len(result)

    else:
        raise Exception('missing determination method by parameter -d --determination = ml or dist')

    sorted_df = df.sort_values(by='most_likely', ascending=False)

    return get_json(sorted_df, log_ll, top_n, classes, methods)


def evaluate(text, k1):

    word_list = data.nltk_filter(text)

    if k1:
        mdl = tp.LDAModel().load('{}_{}.mdl'.format(FILE_NAME, k1))
    else:
        mdl = tp.LDAModel().load('{}.mdl'.format(FILE_NAME))

    if word_list:
        doc = mdl.make_doc(word_list)

        return mdl.infer(doc)

    return 'error'


def train(documents, features, topic_n=20):

    mdl = tp.LDAModel(k=topic_n, seed=123, rm_top=20)

    data_list = tomotopy_train(mdl, documents, features)

    for row in data_list:

        doc = mdl.docs[row['model_index']]
        topics = doc.get_topics(top_n=topic_n)
        topics = sorted(topics, key=lambda item: item[0])

        for t in range(topic_n):
            row['topic_{}'.format(t)] = topics[t][1]

    columns = list(data_list[0].keys())
    mapping = pd.DataFrame(data_list, columns=columns)

    # print(res)

    mdl.save('{}_k1{}.mdl'.format(FILE_NAME, topic_n))

    mapping.to_csv('{}.csv'.format(FILE_NAME))

    return {FILE_NAME: mdl.ll_per_word}
