import os
from pymongo import MongoClient
from datetime import date

if not os.path.isdir('repos'):
    os.mkdir('repos')
WORKDIR = os.getcwd()

REPO = {
    'title': 'zookeeper',
    'git-url': 'https://github.com/apache/zookeeper.git',
    'jira-url': 'https://issues.apache.org/jira',
    'end': date(2000, 1, 1)
}


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
