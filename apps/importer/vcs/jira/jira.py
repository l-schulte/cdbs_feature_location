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


def get_features(commits):
    """Get associated feature per commit.

    Features can be any documents in a jira instance linked through the commit message.

    """

    jira_base_url = REPO['jira-url']

    session = __get_session(jira_base_url)

    for commit in progressbar.progressbar(commits):

        res = re.search(r'^\s*(\w+-\d+):', commit['comment'])
        if res:
            commit['feature_id'] = res.group(1)
        else:
            continue

        jira_issue_url = '{}/rest/api/2/issue/{}'.format(jira_base_url, commit['feature_id'])

        response = session.get(jira_issue_url)

        if not response.ok:
            print('Error for url: {}'.format(jira_issue_url))

        data = response.json()

        if 'fields' in data and 'description' in data['fields'] and 'issuetype' in data['fields']:
            commit['feature'] = {
                'description': data['fields']['description'],
                'type': data['fields']['issuetype']
            }
        else:
            print('No data for url: {}'.format(jira_issue_url))

    return commits
