"""Module where all interfaces, events and exceptions live."""

from plone.autoform.interfaces import IFormFieldProvider
from plone.schema import JSONField
from plone.supermodel import model
from zope.interface import provider
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from eea.dexterity.indicators import EEAMessageFactory as _
from eea.schema.slate.field import SlateJSONField


class IEeaDexterityIndicatorsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


@provider(IFormFieldProvider)
class IIndicator(model.Schema):
    """ IMS Indicator schema provider
    """
    model.fieldset(
        "metadata",
        label=_("Metadata"),
        fields=[
            "temporal_coverage",
            "geo_coverage",
        ]
    )

    model.fieldset(
        "euro_sdmx_metadata_structure",
        label=_("Supporting information"),
        fields=[
            "data_provenance",
        ]
    )

    temporal_coverage = JSONField(
        title=_(u"Temporal coverage"),
        description=_(
            "This property is read-only and it is automatically "
            "extracted from this indicator's data visualizations."
        ),
        required=False,
        widget="temporal",
        default={"readOnly": True, "temporal": []}
    )

    geo_coverage = JSONField(
        title=_(u"Geographic coverage"),
        description=_(
            "This property is read-only and it is automatically "
            "extracted from this indicator's data visualizations"
        ),
        required=False,
        widget="geolocation",
        default={"readOnly": True, "geolocation": []}
    )

    data_provenance = SlateJSONField(
        title=_(u"Data sources and providers"),
        description=_(
            "This property is read-only and it is automatically "
            "extracted from this indicator's data visualizations"
        ),
        required=False,
        default=[]
    )
