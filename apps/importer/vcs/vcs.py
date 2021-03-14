from vcs.jira import jira


def get_features(commits):
    """Get associated feature per commit.

    Currently supports only apache projects hosted on jira.

    """
    return jira.get_features(commits)
