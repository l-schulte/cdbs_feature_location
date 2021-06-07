from issues.jira import jira

SYSTEM = jira


def get_features(commits):
    """Get associated feature per commit.

    Currently supports only apache projects hosted on jira.

    """
    return SYSTEM.get_features(commits)


def get_feature_id(comment):
    return SYSTEM.get_feature_id(comment)
