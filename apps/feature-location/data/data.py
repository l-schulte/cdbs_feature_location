import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

stop_words = stopwords.words('english')


def get_db():
    from pymongo import MongoClient

    MONGODB_ADDR = 'localhost'

    client = MongoClient('mongodb://%s:%s@%s' %
                         ('root', 'localdontuseglobal', MONGODB_ADDR))

    db = client.cdbs_fl_db
    db_commits = db.commits

    db_commits.create_index('date')

    return db_commits


def nltk_doc_filter(doc):

    if not ('feature' in doc and 'description' in doc['feature'] and doc['feature']['description']):
        return None

    text = doc['feature']['description']

    return nltk_filter(text)


def nltk_filter(text):

    text = text.lower()

    text_tokens = word_tokenize(text)
    remove_sw = [word for word in text_tokens if word not in stop_words and word.isalpha()]

    return remove_sw
