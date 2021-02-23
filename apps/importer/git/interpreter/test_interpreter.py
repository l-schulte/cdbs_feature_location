import unittest
from git.interpreter import interpreter

FILE_CHUNK_DIFF = """
 def crawl(repo):
 def get_diff(commit_id, steps_back=1):

-    parameters = ['--histogram']
-
-    return cli.diff(commit_id, steps_back, parameters)
+    return cli.diff(commit_id, steps_back, DIFF_PARAMETERS)


 def get_file_content(commit_id, path):"""


class TestInterpreter(unittest.TestCase):

    def test_interpret_file_chunk_diff(self):

        path = 'dummy.py'
        lines = FILE_CHUNK_DIFF.splitlines()

        res = interpreter._interpret_file_chunk_diff(path, lines, 0, 0)

        self.assertEqual(res, {'unknown': 0, 'crawl': 0, 'get_diff': 3, 'get_file_content': 0})
