import os
import subprocess

from __init__ import b2s, REPO, WORKDIR

from sys import platform

shell = not platform == 'win32'


def clone():
    """Clone the repository this instance is assigned to.

    """

    os.chdir('repos')

    command = 'git clone {}'.format(REPO['git-url'])
    _ = subprocess.run(command, capture_output=True, shell=shell)

    os.chdir(WORKDIR)


def checkout(commit_id):
    """Checkout a specific commit of the repository this instance is assigned to.

    """

    os.chdir('repos/{}'.format(REPO['title']))

    command = 'git checkout {}'.format(commit_id)
    res = subprocess.run(command, capture_output=True, shell=shell)

    os.chdir(WORKDIR)

    return res


def diff(commit_id, parameters=[]):
    """Performs a diff operation on two versions of the repository

    """

    os.chdir('repos/{}'.format(REPO['title']))

    parameters = ' '.join(parameters)
    command = 'git diff {}^ {} {}'.format(commit_id, commit_id, parameters)
    res = subprocess.run(command, capture_output=True, shell=shell)

    os.chdir(WORKDIR)

    return b2s(res.stdout).splitlines()


def pull():
    """Pull all branches from the repository this instance is assigned to.

    """

    os.chdir('repos/{}'.format(REPO['title']))

    command = 'git pull --all'
    _ = subprocess.run(command, capture_output=True, shell=shell)

    os.chdir(WORKDIR)


def log():
    """Return the logs of the repository.

    """

    os.chdir('repos/{}'.format(REPO['title']))

    command = 'git log --numstat --no-merges --date=unix --after={} --before={}'.format(REPO['after'], REPO['before'])
    print(command)
    res = subprocess.run(command, capture_output=True, shell=shell)

    os.chdir(WORKDIR)

    return b2s(res.stdout).splitlines()


def show(commit_id, path):
    """Return the contents of a version of a file as a string.

    """

    os.chdir('repos/{}'.format(REPO['title']))

    command = 'git show {}:{}'.format(commit_id, path)
    res = subprocess.run(command, capture_output=True, shell=shell)

    os.chdir(WORKDIR)

    if res.returncode == 0:
        return b2s(res.stdout)
    else:
        return ''
