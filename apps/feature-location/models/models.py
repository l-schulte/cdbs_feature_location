import json
from data import data


def tomotopy_train(mdl) -> list:
    db_commits = data.get_db()

    data_list = []

    for document in db_commits.find(limit=1000).where('this.diff.length > 0'):
        word_list = data.nltk_doc_filter(document)
        if word_list:
            idx = mdl.add_doc(word_list)
            tmp = {
                'id': str(document['_id']),
                'feature': document['feature_id'],
                'mapping': json.dumps(document['diff']),
                'model_index': idx
            }
            data_list.append(tmp)

    for i in range(0, 100, 10):
        mdl.train(10)
        # print('Iteration: {}\tLog-likelihood: {}'.format(i, mdl.ll_per_word))

    # for k in range(mdl.k2):
    #     print('Top 10 words of topic #{}'.format(k))
    #     print(mdl.get_topic_words(k, top_n=3))

    # mdl.summary()

    return data_list


def get_page(df, top_n, classes, methods):
    res = []
    cnt = 0
    for row in df.mapping[0:top_n]:
        cnt += 1
        data = json.loads(row)

        res.append('- {} -'.format(cnt))

        if len(data) == 0:
            res.append(' x')

        for item in data:
            res.append(' {}'.format(item['new_path'][1:]))

            if methods:
                for method in sorted(item['methods'], key=lambda x: item['methods'][x], reverse=True):
                    res.append('  ->  {} ({})'.format(method, item['methods'][method]))

            if classes:
                for c in item['classes']:
                    res.append('  •  {}'.format(c))

    return '\n'.join(res)


def get_json(df, log_ll, top_n, classes, methods):

    res = {'log_ll': log_ll, 'res': []}

    for id, mapping in zip(df.id[0:top_n], df.mapping[0:top_n]):
        mapping = json.loads(mapping)
        commit = {'commit_id': id, 'files': []}

        for item in mapping:
            file = {'path': item['new_path'][1:]}

            if methods:
                file['methods'] = {}
                for method in sorted(item['methods'], key=lambda x: item['methods'][x], reverse=True):
                    file['methods'][method] = item['methods'][method]

            if classes:
                file['classes'] = item['classes']

            commit['files'].append(file)

        res['res'].append(commit)

    return json.dumps(res, indent=4)
