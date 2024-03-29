from typing import List
from data import get_db_files
import json
import os
from bson import json_util
from nltk.tokenize import word_tokenize

from data import stopwords


class Document:
    _id: str
    name: str
    path: str
    feature_ids: List[str]
    diffs: List[str]

    def __init__(self, _id, name: str, path: str, feature_ids: List[str], diffs: List[any]):
        self._id = _id
        self.name = name
        self.path = path
        self.feature_ids = feature_ids

        self.diffs = []
        for diff in diffs:
            self.diffs.append({
                '+': nltk_filter(diff['+']),
                '-': nltk_filter(diff['-']),
                '=': nltk_filter(diff['='])
            })

    def get_word_list(self, features, diff_type=['+', '=']):
        word_list = []

        for feature_id in self.feature_ids:
            if feature_id in features:
                word_list.extend(features[feature_id]['words'])

        for diff in self.diffs:
            for t in diff_type:
                word_list.extend(diff[t])

        return word_list


def get_files():
    files = {}
    file_cache = 'files_cache.json'
    if os.path.isfile(file_cache):
        f = open(file_cache, 'r')
        files = json_util.loads(f.read())
        f.close()
    else:
        files = list(get_db_files().find())
        f = open(file_cache, 'w')
        json.dump(files, f, indent=4, default=json_util.default)
        f.close()

    return files


def get_documents(type) -> List[Document]:

    documents = []
    if type == 'file':
        for file in get_files():
            name = file['path'].split('/')[-1].split('.')[0]
            documents.append(Document(str(file['_id']), name, file['path'], file['feature_ids'], None))
        return documents

    if type == 'class':
        for file in get_files():
            classes = {}
            diffs = {}
            if 'changes' in file:
                for change in file['changes']:
                    if 'diff' in change and 'classes' in change['diff']:
                        for class_name in change['diff']['classes']:
                            if class_name == 'unknown' or change['diff']['classes'][class_name]['cnt'] == 0:
                                continue
                            if class_name not in classes:

                                tmp = set()
                                tmp.add(change['feature_id'])
                                classes[class_name] = {
                                    'ids': tmp,
                                    'diffs': [change['diff']['classes'][class_name]]
                                }
                            else:
                                classes[class_name]['ids'].add(change['feature_id'])
                                classes[class_name]['diffs'].append(change['diff']['classes'][class_name])
            for class_name in classes:
                feature_ids = classes[class_name]['ids']
                diffs = classes[class_name]['diffs']
                path = '{} -> {}'.format(file['path'], class_name)
                documents.append(Document(file['_id'], class_name, path, feature_ids, diffs))
        return documents


def nltk_feature_filter(features: dict):

    for feature_id in features:

        if feature_id == '_id':
            continue

        feature = features[feature_id]
        feature['words'] = []
        feature['words'].extend(nltk_filter(feature['description']))
        feature['words'].extend(nltk_filter(feature['title']))

    return features


def nltk_filter(text: str):

    if not text:
        return []

    text = text.lower()

    text_tokens = word_tokenize(text)

    remove_sw = [token for token in text_tokens if token not in stopwords]

    # ps = PorterStemmer()
    # remove_sw = [ps.stem(word) for word in text_tokens if word not in stop_words and word.isalpha()]

    return remove_sw


def read_goldsets(path):

    filenames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    goldsets = []

    for filename in filenames:
        f = open('{}{}'.format(path, filename), 'r')
        lines = f.readlines()
        f.close()

        goldsets.append({
            'file': filename,
            'classes': [line.split('.')[-1].replace('\n', '') for line in lines]
        })

    return goldsets


def read_query_results(path):

    filenames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    results = []

    for filename in filenames:
        f = open('{}{}'.format(path, filename), 'r')
        lines = f.read()
        f.close()

        results.append({
            'file': filename,
            'documents': json.loads(lines)
        })

    return results
