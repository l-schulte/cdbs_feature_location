from git import interpreter, cli, DIFF_PARAMETERS


def crawl(repo):
    """Crawl the repository returning codebase history data.

    """

    cli.clone()
    cli.pull()
    cli.checkout(repo['start'])

    log = cli.log()
    return interpreter.log(log)


def get_diff(commit_id, steps_back=1):
    """Returns contents of a git diff operation

    """

    return cli.diff(commit_id, steps_back, DIFF_PARAMETERS)


def get_file_content(commit_id, path):
    """Returns the contents of a version of a file as a string.

    """

    return cli.show(commit_id, path)


def checkout_commit(repo, commit_id):
    """Checkout a specific version of the repository.

    """

    return cli.checkout(commit_id)
