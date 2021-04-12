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
    'after': date(2000, 1, 1),
    'before': date(2012, 11, 19)
}


MONGODB_ADDR = 'localhost'
MONGODB_ADDR_ATLAS = 'cluster0.57xhr.mongodb.net/?retryWrites=true&w=majority'
MONGODB_USER_ATLAS = 'app'
MONGODB_PWD_ATLAS = 'M5Aks6FW2bKDVbG'

client = MongoClient('mongodb+srv://{}:{}@{}'.format(MONGODB_USER_ATLAS, MONGODB_PWD_ATLAS, MONGODB_ADDR_ATLAS))

db = client[REPO['title']]
db_commits = db.commits
db_files = db.files
db_features = db.features

db_commits.create_index('date')


def b2s(byte):
    """Converts bytes to string.

    Used throughout the tool in combination with return values from subprocess.run()

    """

    return '' if not byte else byte.decode("utf-8", errors="ignore")
