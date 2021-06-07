from copy import Error
import re
from datetime import datetime
from issues.issues import get_feature_id
import progressbar

from git.interpreter import LANGUAGE_REGX


def __join_json(j1, j2):
    """Summs up fields from two jsons, assuming values are {'cnt': int}

    """

    if j2 is None:
        return j1

    for key in j2:
        if key in j1:
            j1[key]['cnt'] += j2[key]['cnt']
            j1[key]['+'] += j2[key]['+']
            j1[key]['-'] += j2[key]['-']
            j1[key]['='] += j2[key]['=']
        else:
            j1[key] = j2[key]

    return j1


def log(log):
    """Read a git log and return all commits.

    """

    commits = []
    changes = []

    line_buffer = []
    for line in progressbar.progressbar(log):

        if re.search(r'^commit .+', line) and not line_buffer == []:

            commit = __interpret_commit(line_buffer)
            commits.append(commit)

            changes.extend(__interpret_changes(line_buffer, commit['commit_id'], commit['feature_id']))

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
        'comment': comment,
        'feature_id': get_feature_id(comment)
    }


def __interpret_changes(lines, commit_id, feature_id):
    """Extract data from change lines using regex.
    """

    changes = []

    for line in lines[4:]:

        rline = re.search(r'^\d+\s+\d+\s+(.+)', line)
        if rline:

            path_change = re.search(r'(.*){(.*) => (.*)}(.*)', rline.group(1))

            if path_change:
                path = (path_change.group(1)
                        + path_change.group(3) + path_change.group(4)).replace('//', '/')
                old_path = (path_change.group(1)
                            + path_change.group(2) + path_change.group(4)).replace('//', '/')
            else:
                path = rline.group(1)
                old_path = rline.group(1)

            changes.append({
                'commit_id': commit_id,
                'feature_id': feature_id,
                'path': path,
                'old_path': old_path
            })

    return changes


def crawl_diff(diff):
    """Read a git diff and return information on methods that have been changed

    """

    changes = {}

    old_path = None
    new_path = None
    line_buffer = []

    for line in diff:

        if re.search(r'^diff --git .+', line):

            if not line_buffer == []:

                extension = new_path.split('.')[-1]
                if extension in LANGUAGE_REGX:

                    methods, classes = _interpret_file_diff(line_buffer, extension)

                    changes[new_path[2:]] = {
                        'old_path': old_path[2:],
                        'classes': classes,
                        'methods': methods
                    }

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

    methods = {}

    for line in lines:

        r_chunk_head = re.search(r'^@@ -(\d+),\d+ \+(\d+),\d+ @@ (.*)', line)
        if r_chunk_head:
            methods_changed, classes_in_file = _interpret_file_chunk_diff(extension, chunk_line_buffer,
                                                                          chunk_head_old_start_line,
                                                                          chunk_head_new_start_line)
            methods = __join_json(methods, methods_changed)

            chunk_head_old_start_line = r_chunk_head.group(1)
            chunk_head_new_start_line = r_chunk_head.group(2)
            chunk_line_buffer = [r_chunk_head.group(3)]

        else:
            chunk_line_buffer.append(line)

    methods_changed, classes_in_file = _interpret_file_chunk_diff(extension, chunk_line_buffer,
                                                                  chunk_head_old_start_line, chunk_head_new_start_line)
    methods = __join_json(methods, methods_changed)

    return methods, classes_in_file


def _interpret_file_chunk_diff(extension, lines, old_start, new_start):
    """Extract changed methods from a git diff chunk using regex.

    """

    if lines == []:
        return {}, {}

    re_method_name = None
    if extension in LANGUAGE_REGX:
        re_method_name = LANGUAGE_REGX[extension]['method_name']
        re_class_name = LANGUAGE_REGX[extension]['class_name']
        brackets_open = LANGUAGE_REGX[extension]['brackets_open']
        brackets_close = LANGUAGE_REGX[extension]['brackets_close']
    else:
        return {}, {}

    methods_changed = __interpret_changed_methods(lines, re_method_name)
    classes_in_file = __interpret_changed_classes(lines, re_class_name, brackets_open, brackets_close)

    return methods_changed, classes_in_file


def __interpret_changed_methods(lines, re_method_name):

    methods_changed = {'unknown': {'cnt': 0, '+': '', '-': '', '=': ''}}
    method_name = None
    method_indentation = None

    for line in lines:

        if line == '' or re.search(r'^[\+|\-]$', line):
            continue

        re_res_method_changed = None
        if re_method_name:
            re_res_method_changed = re.search(re_method_name, line)
        if re_res_method_changed is not None:

            changed = re_res_method_changed.group(1)
            method_indentation = re_res_method_changed.group(2)
            method_name = re_res_method_changed.group(3)

            methods_changed[method_name] = {'cnt': 0, '+': '', '-': '', '=': ''}

            if changed != ' ':
                methods_changed[method_name]['cnt'] += 1
                methods_changed[method_name][changed] += line
            else:
                methods_changed[method_name]['='] += line

            continue

        if method_name is not None and method_indentation is not None:

            change_inside = re.search(r'^(\+|\-| )' + method_indentation + r'(\t+| +)(.*)', line)
            if change_inside is not None and change_inside.group(1) != ' ':
                methods_changed[method_name]['cnt'] += 1
                methods_changed[method_name][change_inside.group(1)] += change_inside.group(3)
                continue
            else:
                methods_changed[method_name]['='] += line

        re_res_unknown_changed = re.search(r'^(\+|\-| )(\t+| +)(.*)', line)
        if re_res_unknown_changed is not None and re_res_unknown_changed.group(1) != ' ':

            methods_changed['unknown']['cnt'] += 1
            methods_changed['unknown'][re_res_unknown_changed.group(1)] += re_res_unknown_changed.group(3)
            method_name = None
            method_indentation = None

            continue
        else:
            methods_changed['unknown']['='] += line

    return methods_changed


def __interpret_changed_classes(lines, re_class_name, brackets_open, brackets_close):

    classes_changed = {'unknown': {'cnt': 0, '+': '', '-': '', '=': ''}}
    class_name = 'unknown'
    brackets_count = 0

    for line in lines:

        if line == '' or re.search(r'^[\+|\-]$', line):
            continue

        re_res_class_name = None
        if re_class_name and brackets_count == 0:
            re_res_class_name = re.search(re_class_name, line)
        if re_res_class_name is not None:
            changed = re_res_class_name.group(1)
            class_name = re_res_class_name.group(3)

            classes_changed[class_name] = {'cnt': 0, '+': '', '-': '', '=': ''}
            if changed != ' ':
                classes_changed[class_name]['cnt'] += 1
                classes_changed[class_name][changed] += line
            else:
                classes_changed[class_name]['='] += line

            brackets_count = line.count(brackets_open) - line.count(brackets_close)

            continue

        brackets_count += line.count(brackets_open) - line.count(brackets_close)
        change_inside = re.search(r'^(\+|\-| )(.*)', line)
        if change_inside is not None and change_inside.group(1) != ' ':
            classes_changed[class_name]['cnt'] += 1
            classes_changed[class_name][change_inside.group(1)] += change_inside.group(2)
            continue
        else:
            classes_changed[class_name]['='] += line

    return classes_changed
