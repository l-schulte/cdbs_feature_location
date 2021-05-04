import progressbar
import os
import json

from __init__ import db_commits, db_files, db_features, REPO
from git import git
from issues import issues


def __get_commits():
    return list(db_commits.find())


def __store_changes(changes, diffs):
    """Stores changes found in repository.

    """

    for change in progressbar.progressbar(changes):

        if change['commit_id'] in diffs:
            diff = diffs[change['commit_id']]
            if change['path'] in diff:
                file_diff = diff[change['path']]
                change['diff'] = file_diff
            # else:
            #     print('no diff in commit {} for file {}'.format(change['commit_id'], change['path']))
            #     print(diff)

        prev_file = db_files.find_one({
            'tmp_path': change['path']
        })

        if prev_file:
            feature_ids = set(prev_file['feature_ids'])
            feature_ids.add(change['feature_id'])
            db_files.update_one({
                '_id': prev_file['_id']
            }, {
                '$set': {
                    'tmp_path': change['old_path'],
                    'feature_ids': list(feature_ids)
                },
                '$push': {
                    'changes': change
                }
            }, True)

            file_id = prev_file['_id']
        else:
            res = db_files.insert_one({
                'path': change['path'],
                'tmp_path': change['old_path'],
                'feature_ids': [change['feature_id']],
                'changes': [change]
            })

            file_id = res.inserted_id

        db_commits.update_one({
            'commit_id': change['commit_id']
        }, {
            '$push': {
                'files': {
                    'id': file_id,
                    'path': change['path']
                }
            }
        })


def go():
    """

    """

    print('Cloning repo...')
    git.clone_repo()

    print('Crawling commits...')
    commits, changes = git.crawl_commits(REPO)

    print('Crawling diffs...')
    diffs = {}
    for commit in progressbar.progressbar(commits):
        diff = git.crawl_diff(commit['commit_id'])
        diffs[commit['commit_id']] = diff

    # commits = get_commits()

    print('Crawling features...')
    features = {}
    feature_cache = 'features_{}_{}_{}.json'.format(REPO['title'], REPO['after'], REPO['before'])
    if os.path.isfile(feature_cache):
        f = open(feature_cache, 'r')
        features = json.loads(f.read())
        f.close()
    else:
        features = issues.get_features(commits)
        f = open(feature_cache, 'w')
        json.dump(features, f, indent=4)
        f.close()

    print('Saving...')
    db_commits.insert_many(commits)
    __store_changes(changes, diffs)
    db_features.insert_one(features)


go()
