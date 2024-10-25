"""Upgrade step to upgrade indicators to the new embed block"""

import logging
import json
import transaction
from zope.lifecycleevent import modified
from plone.restapi.blocks import visit_blocks


logger = logging.getLogger("upgrade_dataFigure")
logger.setLevel(logging.INFO)


def convert_dataFigure_to_embed_content(block_data):
    "Convert block_data to embed_content"
    embed_content = block_data.copy()

    embed_content["@type"] = "embed_content"
    return embed_content


def upgrade_data_figure(portal):
    """Upgrade all dataFigure blocks to embed_content"""
    i = 0
    for brain in portal.portal_catalog(
        portal_type=["ims_indicator"],
        object_provides="plone.restapi.behaviors.IBlocks",
    ):
        obj = brain.getObject()
        blocks = obj.blocks
        logger.info("Processing %s", obj.absolute_url())
        # retrive block data from the item
        for block in visit_blocks(obj, blocks):
            if block.get("@type", False) and block["@type"] == "dataFigure":
                new_block = block.copy()
                new_block = convert_dataFigure_to_embed_content(block)
                block.clear()
                block.update(new_block)
                logger.info("%s - Updated", obj.absolute_url())

        obj.blocks = blocks
        modified(obj)
        i += 1
        if not i % 100:
            logger.info(i)
            transaction.commit()
    transaction.commit()
