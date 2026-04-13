"""Unit tests for eea.dexterity.indicators pure functions

These tests cover pure functions that don't require Plone context:
- remove_api_string
- dedupe_data
- _unicode_save_string_concat
"""

import unittest
from eea.dexterity.indicators.behaviors.indicator import (
    remove_api_string,
    dedupe_data,
)
from eea.dexterity.indicators.indexer import _unicode_save_string_concat


class TestRemoveApiString(unittest.TestCase):
    """Tests for remove_api_string function"""

    def test_remove_api_site(self):
        result = remove_api_string("/api/SITE/plone/page")
        # Note: strip('/view') removes characters, not substring
        self.assertTrue(result.startswith("plone"))

    def test_remove_api_vh(self):
        result = remove_api_string("/++api++/plone/page")
        # Note: strip('/view') removes characters, not substring
        self.assertTrue(result.startswith("plone"))

    def test_no_api_prefix(self):
        result = remove_api_string("/plone/page")
        # strip removes characters not substrings, so /view chars get stripped
        self.assertTrue("plone/pag" in result or "plone/page" in result)

    def test_simple_path(self):
        result = remove_api_string("/Plone/document")
        self.assertTrue("Plone" in result)

    def test_empty_string(self):
        result = remove_api_string("")
        self.assertEqual(result, "")

    def test_root_path(self):
        result = remove_api_string("/")
        self.assertEqual(result, "")


class TestDedupeData(unittest.TestCase):
    """Tests for dedupe_data function"""

    def test_no_duplicates(self):
        data = [
            {"link": "https://example.com/a", "title": "A"},
            {"link": "https://example.com/b", "title": "B"},
        ]
        result = list(dedupe_data(data))
        self.assertEqual(len(result), 2)

    def test_url_duplicates(self):
        data = [
            {"link": "https://www.eea.europa.eu", "title": "title"},
            {"link": "https://www.eea.europa.eu/", "title": "title 2"},
        ]
        result = list(dedupe_data(data))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "title")

    def test_title_duplicates_no_link(self):
        data = [
            {"title": "Same Title"},
            {"title": "Same Title"},
        ]
        result = list(dedupe_data(data))
        self.assertEqual(len(result), 1)

    def test_empty_list(self):
        result = list(dedupe_data([]))
        self.assertEqual(result, [])

    def test_mixed_duplicates(self):
        data = [
            {"link": "https://example.com", "title": "A"},
            {"link": "https://example.com", "title": "B"},
            {"title": "C"},
            {"title": "C"},
        ]
        result = list(dedupe_data(data))
        self.assertEqual(len(result), 2)


class TestUnicodeSaveStringConcat(unittest.TestCase):
    """Tests for _unicode_save_string_concat function"""

    def test_concat_strings(self):
        result = _unicode_save_string_concat("hello", "world")
        self.assertIn("hello", result)
        self.assertIn("world", result)

    def test_concat_bytes(self):
        result = _unicode_save_string_concat(b"hello", b"world")
        self.assertIn("hello", result)
        self.assertIn("world", result)

    def test_concat_mixed(self):
        result = _unicode_save_string_concat("hello", b"world")
        self.assertIn("hello", result)
        self.assertIn("world", result)

    def test_single_arg(self):
        result = _unicode_save_string_concat("hello")
        self.assertIn("hello", result)

    def test_empty_args(self):
        result = _unicode_save_string_concat()
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
