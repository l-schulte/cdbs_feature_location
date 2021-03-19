import tomotopy as tp
import pandas as pd

from data import db_commits, data

FILE_NAME = 'pa'
TOPICS_K1 = 10
TOPICS_K2 = 10


def evaluate(text):

    mdl = tp.PAModel().load('{}.mdl'.format(FILE_NAME))

    word_list = data.nltk_filter(text)

    if word_list:
        doc = mdl.make_doc(word_list)

        return mdl.infer(doc)

    return 'error'


def train():

    mdl = tp.PAModel(k1=TOPICS_K1, k2=TOPICS_K2, seed=123)

    data_list = []

    for document in db_commits.find(limit=1000):
        word_list = data.nltk_doc_filter(document)
        if word_list:
            idx = mdl.add_doc(word_list)
            tmp = {
                'id': str(document['_id']),
                'feature': document['feature_id'],
                'mapping': document['diff'],
                'model_index': idx
            }
            data_list.append(tmp)

    for i in range(0, 100, 10):
        mdl.train(10)
        print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

    # for k in range(mdl.k2):
    #     print('Top 10 words of topic #{}'.format(k))
    #     print(mdl.get_topic_words(k, top_n=3))

    mdl.summary()

    for row in data_list:

        doc = mdl.docs[row['model_index']]
        topics = doc.get_topics(top_n=TOPICS_K1)
        topics = sorted(topics, key=lambda item: item[0])

        for t in range(TOPICS_K1):
            row['topic_{}'.format(t)] = topics[t][1]

        sub_topics = doc.get_sub_topics(top_n=TOPICS_K2)
        sub_topics = sorted(sub_topics, key=lambda item: item[0])

        for t in range(TOPICS_K2):
            row['sub_topic_{}'.format(t)] = sub_topics[t][1]

    columns = ['id', 'feature', 'mapping', 'model_index']
    columns.extend(['topic_{}'.format(t) for t in range(TOPICS_K1)])
    columns.extend(['sub_topic_{}'.format(t) for t in range(TOPICS_K2)])
    mapping = pd.DataFrame(data_list, columns=columns)

    # print(res)

    mdl.save('{}.mdl'.format(FILE_NAME))

    mapping.to_csv('{}.csv'.format(FILE_NAME))
