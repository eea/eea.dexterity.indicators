"""Tests for the default Indicator block layout."""

import unittest

from eea.dexterity.indicators.interfaces import IIndicatorLayout


class TestIndicatorLayout(unittest.TestCase):
    """Tests for Indicator layout constraints."""

    def test_first_level_blocks_do_not_allow_new_blocks(self):
        blocks = IIndicatorLayout["blocks"].default
        blocks_layout = IIndicatorLayout["blocks_layout"].default

        for block_id in blocks_layout["items"]:
            self.assertTrue(
                blocks[block_id].get("disableNewBlocks"),
                "%s should not allow new first-level blocks" % block_id,
            )

    def test_assessment_groups_keep_nested_slate_blocks_allowed(self):
        blocks = IIndicatorLayout["blocks"].default

        aggregate_assessment = blocks["1bc4379d-cddb-4120-84ad-5ab025533b12"]
        disaggregate_assessment = blocks["d060487d-88fc-4f7b-8ea4-003f14e0fb0c"]

        self.assertEqual(aggregate_assessment["allowedBlocks"], ["slate"])
        self.assertEqual(disaggregate_assessment["allowedBlocks"], ["slate"])


if __name__ == "__main__":
    unittest.main()
