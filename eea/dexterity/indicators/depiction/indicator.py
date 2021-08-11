""" Indicator depcition
"""
import logging
from zope.interface import implementer
from eea.depiction.browser.interfaces import IImageView
from eea.depiction.browser.dexterity import DexterityContainerImageView
logger = logging.getLogger("eea.dexterity.indicators")


@implementer(IImageView)
class IndicatorImageView(DexterityContainerImageView):
    """ Custom Image View for IMS Indicator
    """
    def __call__(self, scalename='thumb'):
        logger.warn("Depiction by eea.dexterity.indicators")
        return super(IndicatorImageView, self).__call__(scalename)
