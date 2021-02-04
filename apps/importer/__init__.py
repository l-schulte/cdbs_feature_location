import os

if not os.path.isdir('repos'):
    os.mkdir('repos')
WORKDIR = os.getcwd()

REPO = {'title': 'JabRef', 'url': 'https://github.com/JabRef/jabref.git'}


def b2s(byte):
    """Converts bytes to string.

    Used throughout the tool in combination with return values from subprocess.run()

    """
    return '' if not byte else byte.decode("utf-8")
