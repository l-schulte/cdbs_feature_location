import requests
import re
import progressbar
from __init__ import REPO


def __get_session(jira_base_url):
    """Prepares requests to have an jira auth cookie.

    """

    session = requests.Session()
    session.get(jira_base_url)
    return session


def get_feature_id(comment):
    res = re.search(r'^\s*(\w+-\d+)\D', comment)
    if res:
        return res.group(1)
    return None


def get_features(commits):
    """Get associated feature per commit.

    Features can be any documents in a jira instance linked through the commit message.

    """

    feature_ids = set()

    for commit in commits:
        feature_id = get_feature_id(commit['comment'])
        if feature_id:
            feature_ids.add(feature_id)

    jira_base_url = REPO['jira-url']

    features = {}

    session = __get_session(jira_base_url)

    for feature_id in progressbar.progressbar(feature_ids):

        jira_issue_url = '{}/rest/api/2/issue/{}'.format(jira_base_url, feature_id)

        response = session.get(jira_issue_url)

        if not response.ok:
            print('Error for url: {}'.format(jira_issue_url))

        data = response.json()

        if 'fields' in data and 'description' in data['fields'] and 'issuetype' in data['fields']:
            features[feature_id] = {
                'description': data['fields']['description'],
                'title': data['fields']['summary'],
                'type': data['fields']['issuetype']
            }
        else:
            print('No data for url: {}'.format(jira_issue_url))

    return features
