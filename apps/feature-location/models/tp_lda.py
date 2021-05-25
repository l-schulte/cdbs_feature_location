from models.models import get_json
import tomotopy as tp
import pandas as pd
import json

FILE_NAME = 'lda'


def create_model(k):
    return tp.LDAModel(k=k, rm_top=20, seed=42), 'lda_{}'.format(k)


def load_model(input, model_name):
    return tp.LDAModel().load('{}{}'.format(input, model_name))


def interpret_evaluation_results(results, path, top_n, determination, k1):

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

    return get_json(sorted_df, log_ll, top_n)


def save_model(mdl, k1, data_list, path, file_prefix):

    for row in data_list:

        doc = mdl.docs[row['model_index']]
        topics = doc.get_topics(top_n=k1)
        topics = sorted(topics, key=lambda item: item[0])

        for t in range(k1):
            row['topic_{}'.format(t)] = topics[t][1]

    columns = list(data_list[0].keys())
    mapping = pd.DataFrame(data_list, columns=columns)

    json.dump(data_list, open('{}/{}.json'.format(path, file_prefix), 'w'), indent=4)
    mapping.to_csv('{}/{}.csv'.format(path, file_prefix))

    return {FILE_NAME: mdl.ll_per_word}
