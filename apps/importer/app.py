import progressbar

from __init__ import db_commits, REPO
from git import git
from vcs import vcs


def get_commits():
    return list(db_commits.find())


def go():
    """

    """

    print('Cloning repo...')
    git.clone_repo()

    print('Crawling commits...')
    commits = git.crawl_commits(REPO)

    print('Crawling diffs...')
    for commit in progressbar.progressbar(commits):
        diff = git.crawl_diff(commit['commit_id'])
        commit['diff'] = diff

    # commits = get_commits()

    print('Crawling features...')
    commits = vcs.get_features(commits)

    print('Saving commits and diffs...')
    db_commits.insert_many(commits)


go()
