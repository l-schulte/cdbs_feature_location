import json


def get_page(df, top_n, classes, methods):
    res = []
    for cnt, path in enumerate(df.path[0:top_n], 1):

        res.append('- {} -'.format(cnt))

        if len(path) == 0:
            res.append(' x')

        res.append(' {}'.format(path))

    return '\n'.join(res)


def get_json(df, log_ll, top_n, classes, methods):

    res = {'log_ll': log_ll, 'res': []}

    for id, path, name in zip(df.id[0:top_n], df.path[0:top_n], df.name[0:top_n]):
        res['res'].append({'_id': id, 'path': path, 'name': name})

    return json.dumps(res, indent=4, sort_keys=False)
