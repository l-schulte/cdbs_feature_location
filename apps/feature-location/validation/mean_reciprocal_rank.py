
def get_rank(goldset, documents):

    for i, document in enumerate(documents['res']):
        if 'classes' in document and any([c in document['classes'] for c in goldset['classes']]):
            # print(i + 1)
            return i + 1

    return len(documents['res'])


def calculate(goldsets, results):

    # print(1/len(results) * sum([get_rank(g, r['documents']) for g, r in zip(goldsets, results)]))

    return 1/len(results) * sum([1/get_rank(g, r['documents']) for g, r in zip(goldsets, results)])
