
def get_rank(goldset, documents):

    files = []
    paths = []

    for commit in documents['res']:
        for file in commit['files']:
            if file['path'] not in paths:
                files.append(file)
                paths.append(file['path'])

    for i, file in enumerate(files, 0):
        if 'classes' in file and any([c in file['classes'] for c in goldset['classes']]):
            return 1/(i + 1)

    return 0


def calculate(goldsets, results):

    # print('len res {}'.format(len(results)))
    # print(1/len(results) * sum([get_rank(g, r['documents']) for g, r in zip(goldsets, results)]))

    return 1/len(results) * sum([(get_rank(g, r['documents'])) for g, r in zip(goldsets, results)])
