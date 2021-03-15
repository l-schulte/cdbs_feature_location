from pymongo import MongoClient


MONGODB_ADDR = 'localhost'

client = MongoClient('mongodb://%s:%s@%s' %
                     ('root', 'localdontuseglobal', MONGODB_ADDR))

db = client.cdbs_fl_db
db_commits = db.commits

db_commits.create_index('date')
