import datetime

from __init__ import db_log
from git import interpreter
from git.cli import GitCli


def crawl(repo):
    """Crawl the repository returning codebase history data.

    """

    db_log.insert_one({'text': 'Import for repo {}'.format(repo['title']),
                       'time': datetime.datetime.now()})

    cli = GitCli(repo)

    cli.clone()
    cli.pull()
    cli.checkout(repo['start'])

    log = cli.log()
    return interpreter.log(log)


def get_file_content(repo, commit_id, path):
    """Returns the contents of a version of a file as a string.

    """

    cli = GitCli(repo)

    return cli.show(commit_id, path)


def checkout_commit(repo, commit_id):
    """Checkout a specific version of the repository.

    """

    cli = GitCli(repo)

    return cli.checkout(commit_id)
