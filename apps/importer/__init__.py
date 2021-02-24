import os
from pymongo import MongoClient
from datetime import date

if not os.path.isdir('repos'):
    os.mkdir('repos')
WORKDIR = os.getcwd()

REPO = {'title': 'cdbs_hist_kau', 'url': 'https://github.com/l-schulte/cdbs_hist_kau.git', 'end': date(2020, 1, 1)}


MONGODB_ADDR = 'db'

client = MongoClient('mongodb://%s:%s@%s' %
                     ('root', 'localdontuseglobal', MONGODB_ADDR))

db = client.cdbs_fl_db
db_commits = db.commits

db_commits.create_index('date')


def b2s(byte):
    """Converts bytes to string.

    Used throughout the tool in combination with return values from subprocess.run()

    """

    return '' if not byte else byte.decode("utf-8", errors="ignore")
