""" indexer.py """
from plone.indexer import indexer
from eea.dexterity.indicators.interfaces import IIndicator
from eea.dexterity.indicators.interfaces import IIndicatorMetadata


@indexer(IIndicator)
def data_provenance_indexer(obj):
    """Data Provenance indexer"""
    data_provenance = IIndicatorMetadata(obj).data_provenance

    if not data_provenance or "data" not in data_provenance:
        return None
    data = {}
    for val in data_provenance['data']:
        data[val["organisation"]] = val["organisation"]

    return data


@indexer(IIndicator)
def temporal_coverage_indexer(obj):
    """Temporal coverage indexer"""

    temporal_coverage = IIndicatorMetadata(obj).temporal_coverage
    if not temporal_coverage or "temporal" not in temporal_coverage:
        return None

    data = {}
    for val in temporal_coverage["temporal"]:
        data[val["value"]] = val["label"]

    return data
