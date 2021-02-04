import os
import subprocess
import datetime

from __init__ import db_log, b2s
from git import workdir


class GitCli:

    def __init__(self, repo):
        self.repo = repo

    def clone(self):
        """Clone the repository this instance is assigned to.

        """

        os.chdir('repos')

        command = 'git clone {}'.format(self.repo['url'])
        res = subprocess.run(command, capture_output=True, shell=True)

        db_log.insert_one({'text': command,
                           'time': datetime.datetime.now(),
                           'data': {
                               'repo': self.repo['_id'],
                               'error': b2s(res.stderr),
                               'output': b2s(res.stdout)
                           }})

        os.chdir(workdir)

    def checkout(self, commit_id):
        """Checkout a specific commit of the repository this instance is assigned to.

        """

        os.chdir('repos/{}'.format(self.repo['title']))

        command = 'git checkout {}'.format(commit_id)
        res = subprocess.run(command, capture_output=True, shell=True)

        os.chdir(workdir)

        return res

    def pull(self):
        """Pull all branches from the repository this instance is assigned to.

        """

        os.chdir('repos/{}'.format(self.repo['title']))

        command = 'git pull --all'
        res = subprocess.run(command, capture_output=True, shell=True)

        db_log.insert_one({'text': command,
                           'time': datetime.datetime.now(),
                           'data': {
                               'repo': self.repo['_id'],
                               'error': b2s(res.stderr),
                               'output': b2s(res.stdout)
                           }})

        os.chdir(workdir)

    def log(self):
        """Return the logs of the repository.

        """

        os.chdir('repos/{}'.format(self.repo['title']))

        command = 'git log --numstat --no-merges --date=unix --after={}'.format(self.repo['end'].date())
        print(command)
        res = subprocess.run(command, capture_output=True, shell=True)

        os.chdir(workdir)

        return b2s(res.stdout).splitlines()

    def show(self, commit_id, path):
        """Return the contents of a version of a file as a string.

        """

        os.chdir('repos/{}'.format(self.repo['title']))

        command = 'git show {}:{}'.format(commit_id, path)
        res = subprocess.run(command, capture_output=True, shell=True)

        os.chdir(workdir)

        if res.returncode == 0:
            return b2s(res.stdout)
        else:
            return ''
