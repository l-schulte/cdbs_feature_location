from models import lda, pachinko

# lda.train()

# pachinko.train()

text = 'Stat enchaned to include num of children and size'

print('----- LDA')

res = lda.evaluate(text)

print(res)

# print('----- Pachinko')

# res = pachinko.evaluate(text)

# print(res)

# # test_doc = mdl.make_doc('junit quote follower time thread'.split())
# test_doc = mdl.docs[0]

# print(test_doc)

# topic_dist, ll = mdl.infer(test_doc)
# print("Topic Distribution for Unseen Docs: ", topic_dist)
# print("Log-likelihood of inference: ", ll)

# print('done')
