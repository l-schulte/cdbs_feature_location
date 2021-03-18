import tomotopy as tp
import pandas as pd

from data import db_commits, data

FILE_NAME = 'lda'
TOPICS = 20


def run():

    mdl = tp.LDAModel(k=TOPICS, seed=123)

    data_list = []

    for document in db_commits.find(limit=1000):
        word_list = data.nltk_filter(document)
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

    for k in range(mdl.k):
        print('Top 10 words of topic #{}'.format(k))
        print(mdl.get_topic_words(k, top_n=3))

    mdl.summary()

    for row in data_list:

        doc = mdl.docs[row['model_index']]
        topics = doc.get_topics(top_n=TOPICS)
        topics = sorted(topics, key=lambda item: item[0])

        for t in range(TOPICS):
            row['topic_{}'.format(t)] = topics[t][1]

    columns = ['id', 'feature', 'mapping', 'model_index']
    columns.extend(['topic_{}'.format(t) for t in range(TOPICS)])
    mapping = pd.DataFrame(data_list, columns=columns)

    # print(res)

    mdl.save('{}.mdl'.format(FILE_NAME))

    mapping.to_csv('{}.csv'.format(FILE_NAME))
