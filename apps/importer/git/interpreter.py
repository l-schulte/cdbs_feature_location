from copy import Error
import re
from datetime import datetime
import progressbar


def log(log):
    """Read a git log and return all commits and changes.

    """

    commits = []
    changes = []

    line_buffer = []
    for line in progressbar.progressbar(log):

        if re.search(r'^commit .+', line) and not line_buffer == []:

            commit, commit_id, date = __interpret_commit(line_buffer)
            commits.append(commit)

            changes.extend(__interpret_changes(line_buffer, commit_id, date))

            line_buffer = []

        line_buffer.append(line)

    return commits, changes


def __interpret_commit(lines):
    """Extract data from a commit line using regex.

    """

    id = re.search(r'^commit (.+)', lines[0]).group(1)

    if id is None:
        raise Error('no match for id in line {}'.format(lines[0]))

    tmp = re.search(r'^Author: (.+) <(.+)?>', lines[1])

    if tmp is None:
        raise Error('no match for author in line {}'.format(lines[1]))

    author = tmp.group(1)
    email = tmp.group(2)

    tmp = int(re.search(r'^Date: (.+)', lines[2]).group(1))

    if tmp is None:
        raise Error('no match for date in line {}'.format(lines[1]))

    date = datetime.fromtimestamp(tmp)

    comment = ''
    for line in lines[4:]:
        if line.startswith('    ') or line == '':
            comment += str(line + '\n')
        else:
            break

    return {
        'commit_id': id,
        'author': author,
        'email': email,
        'date': date,
        'comment': comment
    }, id, date


def __interpret_changes(lines, commit_id, date):
    """Extract data from change lines using regex.

    """

    changes = []

    for line in lines[4:]:

        rline = re.search(r'^(\d+)\s+(\d+)\s+(.+)', line)
        if rline:
            added = rline.group(1)
            removed = rline.group(2)

            path_change = re.search(r'(.*){(.*) => (.*)}(.*)', rline.group(3))

            if path_change:
                path = (path_change.group(1)
                        + path_change.group(3) + path_change.group(4)).replace('//', '/')
                old_path = (path_change.group(1)
                            + path_change.group(2) + path_change.group(4)).replace('//', '/')
            else:
                path = rline.group(3)
                old_path = rline.group(3)

            changes.append({
                'commit_id': commit_id,
                'date': date,
                'added': added,
                'removed': removed,
                'path': path,
                'old_path': old_path
            })

    return changes
