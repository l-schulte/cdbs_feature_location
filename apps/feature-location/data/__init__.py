from pymongo.collection import Collection


db = None


def __init_db():
    global db
    from pymongo import MongoClient

    MONGODB_ADDR = 'localhost'

    client = MongoClient('mongodb://%s:%s@%s' %
                         ('root', 'localdontuseglobal', MONGODB_ADDR))

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
