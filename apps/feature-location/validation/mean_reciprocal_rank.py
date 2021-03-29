
def get_rank(goldset, documents):
    for i, document in enumerate(documents, 0):
        if any([c in document['name'] for c in goldset['classes']]):
            # print(i+1)
            return 1/(i + 1)

    print(goldset)
    return 0


def calculate(goldsets, results):

    # print('len res {}'.format(len(results)))
    # print(1/len(results) * sum([get_rank(g, r['documents']) for g, r in zip(goldsets, results)]))

    return 1/len(results) * sum([(get_rank(g, r['documents']['res'])) for g, r in zip(goldsets, results)])
