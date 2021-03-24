import json


def draw_page(df, top_n, classes, methods):
    cnt = 0
    for row in df.mapping[0:top_n]:
        cnt += 1
        data = json.loads(row)

        print('- {} -'.format(cnt))

        if len(data) == 0:
            print(' x')

        for item in data:
            print(' {}'.format(item['new_path'][1:]))

            if methods:
                for method in sorted(item['methods'], key=lambda x: item['methods'][x], reverse=True):
                    print('  ->  {} ({})'.format(method, item['methods'][method]))

            if classes:
                for c in item['classes']:
                    print('  •  {}'.format(c))
