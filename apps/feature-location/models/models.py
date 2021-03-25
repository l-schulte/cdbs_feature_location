import json


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

    for i in range(top_n):
        data = df.loc[i]
        mapping = json.loads(data.mapping)
        tmp = {'commit_id': data.id}

        for item in mapping:
            tmp['path'] = item['new_path'][1:]

            if methods:
                tmp['methods'] = {}
                for method in sorted(item['methods'], key=lambda x: item['methods'][x], reverse=True):
                    tmp['methods'][method] = item['methods'][method]

            if classes:
                tmp['classes'] = item['classes']

        res['res'].append(tmp)

    return json.dumps(res, indent=4)
