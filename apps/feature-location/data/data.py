import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')


def nltk_filter(doc):

    if not ('feature' in doc and 'description' in doc['feature'] and doc['feature']['description']):
        return None

    text_tokens = word_tokenize(doc['feature']['description'])
    remove_sw = [word for word in text_tokens if word not in stopwords.words()]
    return ' '.join(remove_sw)
