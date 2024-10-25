"""Upgrade step to upgrade indicators to the new embed block"""

import logging
import json
import transaction
from zope.lifecycleevent import modified


logger = logging.getLogger("upgrade_dataFigure")
logger.setLevel(logging.INFO)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # or str(obj)
        return super(DecimalEncoder, self).default(obj)



def upgrade_data_figure(portal):
    """Upgrade SVG dimensions"""
    i = 0
    for brain in portal.portal_catalog(portal_type=["ims_indicator"]):
        obj = brain.getObject()
        logger.info("Processing %s", obj.absolute_url())
        if hasattr(obj, "blocks"):
            blocks_string = json.dumps(obj.blocks,cls=DecimalEncoder).replace(
                "dataFigure", "embed_content"
            )
            obj.blocks = json.loads(blocks_string)
            modified(obj)
            i = i + 1
            if not i % 100:
                logger.info(i)
                transaction.commit()

    transaction.commit()
