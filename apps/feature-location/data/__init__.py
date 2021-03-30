from pymongo.collection import Collection


db = None


def __init_db():
    global db
    from pymongo import MongoClient

    MONGODB_ADDR_ATLAS = 'cluster0.57xhr.mongodb.net/?retryWrites=true&w=majority'
    MONGODB_USER_ATLAS = 'app'
    MONGODB_PWD_ATLAS = 'M5Aks6FW2bKDVbG'

    client = MongoClient('mongodb+srv://{}:{}@{}'.format(MONGODB_USER_ATLAS, MONGODB_PWD_ATLAS, MONGODB_ADDR_ATLAS))

    db = client.cdbs_fl_db


def get_db_commits() -> Collection:

    if not db:
        __init_db()

    return db.commits


def get_db_files() -> Collection:

    if not db:
        __init_db()

    return db.files


def get_db_features() -> Collection:

    if not db:
        __init_db()

    return db.features
