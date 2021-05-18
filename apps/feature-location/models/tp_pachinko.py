from models.models import get_json
import tomotopy as tp
import pandas as pd
import json

FILE_NAME = 'pa'


def create_model(k1, k2):
    return tp.PAModel(k1=k1, k2=k2, rm_top=20), 'pa_{}_{}'.format(k1, k2)


def load_model(input, model_name):
    return tp.PAModel().load('{}{}'.format(input, model_name))


def interpret_evaluation_results(results, path, top_n, determination, k1, k2):

    (super_topics_prob, sub_topics_prob), log_ll = results

    df = pd.read_csv('{}/{}_{}_{}.csv'.format(path, FILE_NAME, k1, k2))

    if determination == 'ml':

        max_value_super = max(super_topics_prob)
        max_index_super = super_topics_prob.tolist().index(max_value_super)

        max_value_sub = max(sub_topics_prob)
        max_index_sub = sub_topics_prob.tolist().index(max_value_sub)

        df['most_likely'] = (df['topic_{}'.format(max_index_super)] + df['sub_topic_{}'.format(max_index_sub)]) / 2

    elif determination == 'dist':

        df['most_likely_super'] = sum([abs(df['topic_{}'.format(i)] - ri)
                                       for i, ri in enumerate(super_topics_prob)]) / len(super_topics_prob)

        df['most_likely_sub'] = sum([abs(df['sub_topic_{}'.format(i)] - ri)
                                     for i, ri in enumerate(sub_topics_prob)]) / len(sub_topics_prob)

        df['most_likely'] = abs(df.most_likely_super - df.most_likely_sub) / 2
        # df['most_likely'] = df['most_likely_sub']

    else:
        raise Exception('missing determination method by parameter -d --determination = ml or dist')

    sorted_df = df.sort_values(by='most_likely', ascending=False)

    return get_json(sorted_df, log_ll, top_n)


def save_model(mdl, k1, k2, data_list, path, file_prefix):
    for row in data_list:

        doc = mdl.docs[row['model_index']]
        topics = doc.get_topics(top_n=k1)
        topics = sorted(topics, key=lambda item: item[0])

        for t in range(k1):
            row['topic_{}'.format(t)] = topics[t][1]

        sub_topics = doc.get_sub_topics(top_n=k2)
        sub_topics = sorted(sub_topics, key=lambda item: item[0])

        for t in range(k2):
            row['sub_topic_{}'.format(t)] = sub_topics[t][1]

    columns = list(data_list[0].keys())
    mapping = pd.DataFrame(data_list, columns=columns)

    json.dump(data_list, open('{}/{}.json'.format(path, file_prefix), 'w'), indent=4)
    mapping.to_csv('{}/{}.csv'.format(path, file_prefix))

    return {FILE_NAME: mdl.ll_per_word}
