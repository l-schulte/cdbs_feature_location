import argparse
import json
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='directory with text files interpretet as input')
parser.add_argument('-t', '--technique', nargs='+', choices=['lda', 'pa'], help='evaluate cluster')
args = parser.parse_args()

f = open('{}optimize_dump.json'.format(args.input), 'r')
results = json.load(f)

for id, doc in results.items():

    print(doc)

    k1 = None
    k2 = None
    technique = ' '.join(args.technique)
    if 'k1' in doc:
        k1 = doc['k1']
    if 'k2' in doc:
        k2 = doc['k2']
    subprocess.run('python app.py -e {} -v {} -i {} --pa_k1 {} --pa_k2 {} --lda_k1 {}'.format(technique,
                                                                                              technique,
                                                                                              args.input,
                                                                                              k1, k2, k1))
