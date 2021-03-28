import nltk
import json
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

stop_words = stopwords.words('english')


def nltk_feature_filter(features: dict):

    for feature_id in features:

        if feature_id == '_id':
            continue

        feature = features[feature_id]
        feature['words'] = nltk_filter(feature['description'])

    return features


def nltk_doc_filter(doc):

    if not ('feature' in doc and 'description' in doc['feature'] and doc['feature']['description']):
        return None

    text = doc['feature']['description']

    return nltk_filter(text)


def nltk_filter(text: str):

    if not text:
        return []

    text = text.lower()

    text_tokens = word_tokenize(text)
    remove_sw = [word for word in text_tokens if word not in stop_words and word.isalpha()]

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
            'classes': [line.split('.')[-1] for line in lines]
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
