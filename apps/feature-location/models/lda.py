import tomotopy as tp

from data import db_commits, data


def run():

    mdl = tp.LDAModel(k=20)
    for word_list in filter(data.nltk_filter, db_commits.find(limit=100)):
        if word_list:
            mdl.add_doc(word_list)

    for i in range(0, 100, 10):
        mdl.train(10)
        print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

    for k in range(mdl.k):
        print('Top 10 words of topic #{}'.format(k))
        print(mdl.get_topic_words(k, top_n=10))

    mdl.summary()

    print('results:')

    print(mdl.make_doc(['author' 'email']).get_words(top_n=10))
