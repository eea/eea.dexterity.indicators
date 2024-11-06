
""" Upgrade to 9.9 """
import logging
from Products.CMFCore.utils import getToolByName
logger = logging.getLogger("eea.dexterity.indicators")


def to_99(context):
    """ Upgrade to 9.9 """
    logger.warning("Reindex IMS indicator SearchableText...")
    ctool = getToolByName(context, "portal_catalog")
    portal_type = "ims_indicator"
    brains = ctool.unrestrictedSearchResults(portal_type=portal_type)
    idx, total = 0, len(brains)
    for idx, brain in enumerate(brains):
        indicator = brain.getObject()
        indicator.reindexObject(idxs=['SearchableText'])
        if idx % 100 == 0:
            logger.warning(
                "Reindex IMS indicator SearchableText...%s/%s", idx, total)
    logger.warning("Reindex IMS indicator SearchableText... %s/%s", idx, total)
