""" Custom behavior for Indicator
"""
from eea.dexterity.indicators.interfaces import IIndicator
from plone.dexterity.interfaces import IDexterityContent
from zope.component import adapter
from zope.interface import implementer


def getAllBlocks(blocks, flat_blocks):
    """ Get a flat list from a tree of blocks
    """
    for block in blocks.values():
        sub_blocks = (
            block.get("data", {}).get("blocks", {}) or
            block.get("blocks", {})
        )
        if sub_blocks:
            return getAllBlocks(sub_blocks, flat_blocks)

        flat_blocks.append(block)
    return flat_blocks


@implementer(IIndicator)
@adapter(IDexterityContent)
class Indicator(object):
    """Automatically extract metadata from blocks"""

    def __init__(self, context):
        self.context = context

    @property
    def temporal_coverage(self):
        """ Get temporal coverage from Data figure blocks
        """
        res = {"readOnly": True, "temporal": []}
        temporal = []
        blocks = getattr(self.context, 'blocks', None) or {}
        for block in getAllBlocks(blocks, []):
            block_temporal = block.get('temporal', [])
            if not block_temporal:
                continue
            for item in block_temporal:
                if item not in temporal:
                    temporal.append(item)

        res['temporal'] = sorted(
            temporal, key=lambda x: x.get("label"))
        return res

    @temporal_coverage.setter
    def temporal_coverage(self, value):
        """ Read-only temporal coverage
        """
        return

    @property
    def geo_coverage(self):
        """ Get geo coverage from Data figure blocks
        """
        res = {"readOnly": True, "geolocation": []}
        geolocation = []
        blocks = getattr(self.context, 'blocks', None) or {}
        for block in getAllBlocks(blocks, []):
            block_geolocation = block.get('geolocation', [])
            if not block_geolocation:
                continue
            for item in block_geolocation:
                geo_item = {
                    "label": item.get("label", ""),
                    "value": item.get("value", "")
                }
                if geo_item not in geolocation:
                    geolocation.append(geo_item)

        res['geolocation'] = sorted(
            geolocation, key=lambda x: x.get("label"))
        return res

    @geo_coverage.setter
    def geo_coverage(self, value):
        """Read-only geographic coverage"""
        return
