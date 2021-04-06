
def get_rank(goldset, documents):
    for i, document in enumerate(documents, 0):
        if any([c in str(document['name']) for c in goldset['classes']]):
            # print(i+1)
            return 1/(i + 1)

    return 0


def calculate(goldsets, results):

    # nested k-fold cross vaidation

    goldsets.extend(goldsets)
    # results = results[:80]

    # print(1/len(results) * sum([get_rank(g, r['documents']) for g, r in zip(goldsets, results)]))

    # for g, r in zip(goldsets, results):
    #     print('{} - {}'.format(g['file'], r['file']))

    return 1/len(results) * sum([(get_rank(g, r['documents']['res'])) for g, r in zip(goldsets, results)])
