import json


def draw_page(df, top_n, functions):
    cnt = 0
    for row in df.mapping[0:top_n]:
        cnt += 1
        data = json.loads(row)

        print('- {} -'.format(cnt))

        if len(data) == 0:
            print(' x')

        for item in data:
            print(' {}'.format(item['new_path'][1:]))

            if not functions:
                continue

            for function in sorted(item['changed_methods'], key=lambda x: item['changed_methods'][x], reverse=True):
                print('\t{} ({})'.format(function, item['changed_methods'][function]))
