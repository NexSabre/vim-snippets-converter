from unittest import TestCase

from main import find_snippet


class TestSnippet(TestCase):
    def test_find_snippet_body_empty_string(self):
        snippet_db = find_snippet()
        for snippet in snippet_db:
            for body in snippet.body:
                self.assertFalse(not len(body), "Empty string was found on the list")
        self.assertTrue(True)
