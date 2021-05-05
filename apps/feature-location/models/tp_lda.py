from models.models import get_json
from training import training
import tomotopy as tp
import pandas as pd
import json

FILE_NAME = 'lda'


def load_model(input, model_name):
    return tp.LDAModel().load('{}{}'.format(input, model_name))


def interpret_evaluation_results(results, path, top_n, classes, methods, determination, k1):

    result, log_ll = results
    df = pd.read_csv('{}/{}_{}.csv'.format(path, FILE_NAME, k1))

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


def train(documents, features, path, topic_n=20):

    mdl = tp.LDAModel(k=topic_n, seed=123, rm_top=20)

    file_prefix = '{}_{}'.format(FILE_NAME, topic_n)

    data_list, mdl, _ = training.train(mdl, documents, features, path, file_prefix)

    for row in data_list:

        doc = mdl.docs[row['model_index']]
        topics = doc.get_topics(top_n=topic_n)
        topics = sorted(topics, key=lambda item: item[0])

        for t in range(topic_n):
            row['topic_{}'.format(t)] = topics[t][1]

    columns = list(data_list[0].keys())
    mapping = pd.DataFrame(data_list, columns=columns)

    # print(res)

    json.dump(data_list, open('{}/{}.json'.format(path, file_prefix), 'w'), indent=4)
    mapping.to_csv('{}/{}.csv'.format(path, file_prefix))

    return {FILE_NAME: mdl.ll_per_word}
