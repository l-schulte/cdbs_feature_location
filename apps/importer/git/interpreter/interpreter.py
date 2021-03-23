from copy import Error
import re
from datetime import datetime
import progressbar

from git.interpreter import LANGUAGE_REGX


def __join_json(j1, j2):
    """Summs up fields from two jsons, assuming values are numbers

    """

    if j2 is None:
        return j1

    for key in j2:
        if key in j1:
            j1[key] += j2[key]
        else:
            j1[key] = j2[key]

    return j1


def log(log):
    """Read a git log and return all commits.

    """

    commits = []

    line_buffer = []
    for line in progressbar.progressbar(log):

        if re.search(r'^commit .+', line) and not line_buffer == []:

            commit, commit_id, date = __interpret_commit(line_buffer)
            commits.append(commit)

            line_buffer = []

        line_buffer.append(line)

    return commits


def __interpret_commit(lines):
    """Extract data from a commit line using regex.

    """

    id = re.search(r'^commit (.+)', lines[0]).group(1)

    if id is None:
        raise Error('no match for id in line {}'.format(lines[0]))

    tmp = re.search(r'^Author: (.+) <(.+)?>', lines[1])

    author, email = None, None

    if tmp is not None:
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


def crawl_diff(diff):
    """Read a git diff and return information on methods that have been changed

    """

    changes = []

    old_path = None
    new_path = None
    line_buffer = []

    for line in diff:

        if re.search(r'^diff --git .+', line):

            if not line_buffer == []:

                extension = new_path.split('.')[-1]
                if extension in LANGUAGE_REGX:
                    
                    changed_methods = _interpret_file_diff(line_buffer, extension)

                    changes.append({
                        'new_path': new_path,
                        'old_path': old_path,
                        'changed_methods': changed_methods
                    })

            old_path = None
            new_path = None
            line_buffer = []
            continue

        if not old_path or not new_path:

            r_old_path = re.search(r'--- (.+)', line)
            if r_old_path:
                old_path = r_old_path.group(1)
                continue
            r_new_path = re.search(r'\+\+\+ (.+)', line)
            if r_new_path:
                new_path = r_new_path.group(1)
                continue

            continue

        if old_path and new_path:
            line_buffer.append(line)

    return changes


def _interpret_file_diff(lines, extension):
    """Extract changed methods from git diff of one file using regex.

    """

    chunk_head_old_start_line = None
    chunk_head_new_start_line = None
    chunk_line_buffer = []

    res = {}

    for line in lines:

        r_chunk_head = re.search(r'^@@ -(\d+),\d+ \+(\d+),\d+ @@ (.*)', line)
        if r_chunk_head:
            methods_changed = _interpret_file_chunk_diff(extension, chunk_line_buffer,
                                                         chunk_head_old_start_line, chunk_head_new_start_line)
            res = __join_json(res, methods_changed)

            chunk_head_old_start_line = r_chunk_head.group(1)
            chunk_head_new_start_line = r_chunk_head.group(2)
            chunk_line_buffer = [r_chunk_head.group(3)]

        else:
            chunk_line_buffer.append(line)

    methods_changed = _interpret_file_chunk_diff(extension, chunk_line_buffer,
                                                 chunk_head_old_start_line, chunk_head_new_start_line)
    res = __join_json(res, methods_changed)

    return res


def _interpret_file_chunk_diff(extension, lines, old_start, new_start):
    """Extract changed methods from a git diff chunk using regex.

    """

    if lines == []:
        return {}

    rs_method_name = None
    if extension in LANGUAGE_REGX:
        rs_method_name = LANGUAGE_REGX[extension]['method_name']
    else:
        return {}

    indentation = None
    method_name = None
    methods_changed = {'unknown': 0}

    for line in lines:

        if line == '' or re.search(r'^[\+|\-]$', line):
            continue

        re_res = None
        if rs_method_name:
            re_res = re.search(rs_method_name, line)
        if re_res is not None:

            changed = re_res.group(1) != ' '
            indentation = re_res.group(2)
            method_name = re_res.group(3)

            if changed:
                methods_changed[method_name] = 1
            else:
                methods_changed[method_name] = 0

            continue

        if method_name is not None and indentation is not None:

            re_res = re.search(r'^(\+|\-| )' + indentation + r'(\t+| +)', line)
            if re_res is not None and re_res.group(1) != ' ':
                methods_changed[method_name] += 1
                continue

        re_res = re.search(r'^(\+|\-| )(\t+| +)', line)
        if re_res is not None and re_res.group(1) != ' ':
            methods_changed['unknown'] += 1
            method_name = None
            indentation = None
            continue

    return methods_changed
