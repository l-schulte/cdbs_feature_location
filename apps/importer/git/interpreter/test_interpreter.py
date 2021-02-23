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


FILE_DIFF = """
diff --git a/apps/importer/git/interpreter/interpreter.py b/apps/importer/git/interpreter/interpreter.py
index 91a0c66..c3103c1 100644
--- a/apps/importer/git/interpreter/interpreter.py
+++ b/apps/importer/git/interpreter/interpreter.py
@@ -6,6 +6,17 @@ import progressbar
 from git.interpreter import LANGUAGE_REGX


+def __join_json(j1, j2):
+
+    for key in j2:
+        if key in j1:
+            j1[key] += j2[key]
+        else:
+            j1[key] = j2[key]
+
+    return j1
+
+
 def log(log):
     \"""Read a git log and return all commits and changes.

@@ -134,74 +145,99 @@ def diff(diff):
 def __interpret_file_diff(lines):
     \"""Extract changed methods from git diff of one file using regex.

     \"""

     old_path = None
     new_path = None

     chunk_head_old_start_line = None
     chunk_head_new_start_line = None
     chunk_line_buffer = []

+    res = {}
+
     for line in lines:

         if not old_path or not new_path:

             r_old_path = re.search(r'--- (.+)', line)
             if r_old_path:
                 old_path = r_old_path.group(1)
                 continue
             r_new_path = re.search(r'\+\+\+ (.+)', line)
             if r_new_path:
                 new_path = r_new_path.group(1)
                 continue

         if old_path and new_path:

             r_chunk_head = re.search(r'^@@ -(\d+),\d+ \+(\d+),\d+ @@ (.*)', line)
-            if r_chunk_head and not chunk_line_buffer == []:
+            if r_chunk_head:

-                res = __interpret_file_chunk_diff(new_path, chunk_line_buffer,
-                                                  chunk_head_old_start_line, chunk_head_new_start_line)
+                methods_changed = _interpret_file_chunk_diff(new_path, chunk_line_buffer,
+                                                             chunk_head_old_start_line, chunk_head_new_start_line)
+
+                res = __join_json(res, methods_changed)

                 chunk_head_old_start_line = r_chunk_head.group(1)
                 chunk_head_new_start_line = r_chunk_head.group(2)
                 chunk_line_buffer = [r_chunk_head.group(3)]

             chunk_line_buffer.append(line)

+    return res

"""

FULL_DIFF = """
diff --git a/apps/importer/git/git.py b/apps/importer/git/git.py
index eaa156d..c431b50 100644
--- a/apps/importer/git/git.py
+++ b/apps/importer/git/git.py
@@ -1,4 +1,4 @@
-from git import interpreter, cli
+from git import interpreter, cli, DIFF_PARAMETERS


 def crawl(repo):
@@ -17,11 +17,9 @@ def crawl(repo):
 def get_diff(commit_id, steps_back=1):
     \"""Returns contents of a git diff operation

     \"""

-    parameters = ['--histogram']
-
-    return cli.diff(commit_id, steps_back, parameters)
+    return cli.diff(commit_id, steps_back, DIFF_PARAMETERS)


 def get_file_content(commit_id, path):
diff --git a/apps/importer/git/interpreter.py b/apps/importer/git/interpreter.py
deleted file mode 100644
index 02efb4d..0000000
--- a/apps/importer/git/interpreter.py
+++ /dev/null
@@ -1,107 +0,0 @@
-from copy import Error
-import re
-from datetime import datetime
-import progressbar
-
-
-def log(log):
-    \"""Read a git log and return all commits and changes.
-
-    \"""
-
-    commits = []
-    changes = []
-
-    line_buffer = []
-    for line in progressbar.progressbar(log):
-
-        if re.search(r'^commit .+', line) and not line_buffer == []:
-
-            commit, commit_id, date = __interpret_commit(line_buffer)
-            commits.append(commit)
-
-            changes.extend(__interpret_changes(line_buffer, commit_id, date))
-
-            line_buffer = []
-
-        line_buffer.append(line)
-
-    return commits, changes
"""


class TestInterpreter(unittest.TestCase):

    def test_interpret_file_chunk_diff(self):

        path = 'dummy.py'
        lines = FILE_CHUNK_DIFF.splitlines()

        res = interpreter._interpret_file_chunk_diff(path, lines, 0, 0)

        self.assertEqual(res, {'unknown': 0, 'crawl': 0, 'get_diff': 3, 'get_file_content': 0})

    def test_interpret_file_diff(self):

        lines = FILE_DIFF.splitlines()

        res = interpreter._interpret_file_diff(lines, 'dummy.py')

        self.assertEqual(res, {'unknown': 0, '__join_json': 7, 'log': 0, '__interpret_file_diff': 9})

    def test_diff(self):

        lines = FULL_DIFF.splitlines()

        res = interpreter.diff(lines)

        self.assertEqual(res, {
            'b/apps/importer/git/git.py': {
                'old_path': 'a/apps/importer/git/git.py',
                'changed_methods': {'unknown': 0, 'crawl': 0, 'get_diff': 3, 'get_file_content': 0}
            }
        })
