import progressbar

from __init__ import db_commits, REPO
from git import git


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

    print('Saving commits and diffs...')
    db_commits.insert_many(commits)


go()
