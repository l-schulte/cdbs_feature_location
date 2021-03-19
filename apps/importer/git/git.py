from git import cli, DIFF_PARAMETERS
from git.interpreter import interpreter


def crawl_commits(repo):
    """Crawl the repository all commits history data.

    """

    log = cli.log()
    return interpreter.log(log)


def crawl_diff(commit_id):
    """Returns contents of a git diff operation

    """
    diff = cli.diff(commit_id, DIFF_PARAMETERS)
    return interpreter.crawl_diff(diff)


def get_file_content(commit_id, path):
    """Returns the contents of a version of a file as a string.

    """

    return cli.show(commit_id, path)


def clone_repo():
    """Clones the repository.

    """

    cli.clone()
    cli.pull()


def checkout_commit(repo, commit_id):
    """Checkout a specific version of the repository.

    """

    return cli.checkout(commit_id)
