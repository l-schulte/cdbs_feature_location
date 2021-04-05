import re
import json

f = open('old_log.txt', 'r')

text = f.read()

logs = re.findall(r'k1: *(\d+) *k2: *(\d+)\n.*\nPA ll per word *(.*)', text)

res = []

for match in logs:

    res.append({
        'k1': match[0],
        'k2': match[1],
        'result': {
            'train': [
                {'pa': float(match[2])}
            ]
        }
    })

json.dump(res, open('log2json_res.txt', 'w'), indent=4)
