import nltk
from pymongo.collection import Collection
from datetime import date
import string

zookeeper = {
    'title': 'zookeeper',
    'git-url': 'https://github.com/apache/zookeeper.git',
    'jira-url': 'https://issues.apache.org/jira',
    'after': date(2000, 1, 1),
    'before': date(2012, 11, 19)
}

tika = {
    'title': 'tika',
    'git-url': 'https://github.com/apache/tika.git',
    'jira-url': 'https://issues.apache.org/jira',
    'after': date(2000, 1, 1),
    'before': date(2013, 1, 19)  # v1.3
}

FOX_STOPS = set(
    """ a about above across after again against all almost alone along already
    also although always among an and another any anybody anyone anything
    anywhere are area areas around as ask asked asking asks at away b back
    backed backing backs be because become becomes became been before began
    behind being beings best better between big both but by c came can cannot
    case cases certain certainly clear clearly come could d did differ different
    differently do does done down downed downing downs during e each early
    either end ended ending ends enough even evenly ever every everybody
    everyone everything everywhere f face faces fact facts far felt few find
    finds first for four from full fully further furthered furthering furthers
    g gave general generally get gets give given gives go going good goods got
    great greater greatest group grouped grouping groups h had has have having
    he her herself here high higher highest him himself his how however i if
    important in interest interested interesting interests into is it its itself
    j just k keep keeps kind knew know known knows l large largely last later
    latest least less let lets like likely long longer longest m made make
    making man many may me member members men might more most mostly mr mrs much
    must my myself n necessary need needed needing needs never new newer newest
    next no non not nobody noone nothing now nowhere number numbered numbering
    numbers o of off often old older oldest on once one only open opened opening
    opens or order ordered ordering orders other others our out over p part
    parted parting parts per perhaps place places point pointed pointing points
    possible present presented presenting presents problem problems put puts
    q quite r rather really right room rooms s said same saw say says second
    seconds see sees seem seemed seeming seems several shall she should show
    showed showing shows side sides since small smaller smallest so some
    somebody someone something somewhere state states still such sure t take
    taken than that the their them then there therefore these they thing things
    think thinks this those though thought thoughts three through thus to today
    together too took toward turn turned turning turns two u under until up upon
    us use uses used v very w want wanted wanting wants was way ways we well
    wells went were what when where whether which while who whole whose why will
    with within without work worked working works would x y year years yet you
    young younger youngest your yours z """.split())

JAVA_RESERVED = set(
    """ abstract assert boolean break byte case catch char class const continue
    default do double else enum extends false final finally float for goto if
    implements import instanceof int interface long native new null package
    private protected public return short static strictfp super switch
    synchronized this throw throws transient true try void volatile while """.split())

stopwords = set()
stopwords.update(FOX_STOPS)
stopwords.update(JAVA_RESERVED)
stopwords.update(string.punctuation)
stopwords.update(string.digits)
stopwords.update(string.whitespace)

nltk.download('punkt', quiet=True)

REPO = zookeeper

db = None


def __init_db():
    global db
    from pymongo import MongoClient

    MONGODB_ADDR_ATLAS = 'cluster0.57xhr.mongodb.net/?retryWrites=true&w=majority'
    MONGODB_USER_ATLAS = 'app'
    MONGODB_PWD_ATLAS = 'M5Aks6FW2bKDVbG'

    client = MongoClient('mongodb+srv://{}:{}@{}'.format(MONGODB_USER_ATLAS, MONGODB_PWD_ATLAS, MONGODB_ADDR_ATLAS))

    db = client[REPO['title']]


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
