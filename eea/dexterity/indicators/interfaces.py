"""Module where all interfaces, events and exceptions live."""

# pylint: disable=line-too-long
from eea.dexterity.indicators import EEAMessageFactory as _
from eea.schema.slate.field import SlateJSONField
from plone.autoform.interfaces import IFormFieldProvider
from plone.restapi.behaviors import BLOCKS_SCHEMA, LAYOUT_SCHEMA
from plone.schema import JSONField, Tuple, Choice
from plone.supermodel import model
from plone.autoform import directives

try:
    from plone.app.z3cform.widgets.select import SelectFieldWidget
except ImportError:
    from z3c.form.browser.select import SelectFieldWidget
from zope.interface import provider, Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import Int


class IEeaDexterityIndicatorsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IIndicator(Interface):
    """Marker interface for IMS Indicator"""


class IIndicatorsFolder(Interface):
    """Marker interface for IMS Folder"""


@provider(IFormFieldProvider)
class IIndicatorMetadata(model.Schema):
    """IMS Indicator schema provider"""

    #
    # Metadata
    #
    model.fieldset(
        "metadata",
        label=_("Metadata"),
        fields=[
            "topics",
            "temporal_coverage",
            "geo_coverage",
        ],
    )

    directives.widget("topics", SelectFieldWidget)
    topics = Tuple(
        title=_("Topics"),
        description=_("Select from the official EEA topics"),
        required=False,
        value_type=Choice(vocabulary="topics_vocabulary"),
        default=(),
    )

    temporal_coverage = JSONField(
        title=_("Temporal coverage"),
        description=_(
            "This property is read-only and it is automatically "
            "extracted from this indicator's data visualizations."
        ),
        required=False,
        widget="temporal",
        default={"readOnly": True, "temporal": []},
    )

    geo_coverage = JSONField(
        title=_("Geographic coverage"),
        description=_(
            "This property is read-only and it is automatically "
            "extracted from this indicator's data visualizations"
        ),
        required=False,
        widget="geolocation",
        default={"readOnly": True, "geolocation": []},
    )

    #
    # Supporting information
    #

    model.fieldset(
        "euro_sdmx_metadata_structure",
        label=_("Supporting information"),
        fields=[
            "methodology",
            "data_provenance",
            "data_description",
            "unit_of_measure",
            "policy_relevance",
            "frequency_of_dissemination",
            "accuracy_and_reliability",
        ],
    )

    methodology = SlateJSONField(
        title=_("Methodology"),
        description=_(
            "Methodology for indicator calculation and for gap filling. "
            "Where relevant, include changes to methodology and subsequent implications for comparability. "
            "Also include uncertainties in relation to the indicator calculation and/or to gap filling) if these are considerable."
        ),
        required=False,
    )

    data_provenance = JSONField(
        title=_("Data sources and providers"),
        description=_(
            "This property is read-only and it is automatically "
            "extracted from this indicator's data visualizations"
        ),
        required=False,
        default={"readOnly": True, "data": []},
    )

    data_description = SlateJSONField(
        title=_("Definition"),
        description=_(
            "Clear definition of the indicator, including references to standards and classifications"
        ),
        required=False,
    )

    unit_of_measure = SlateJSONField(
        title=_("Unit of measure"),
        description=_("Unit in which data values are measured."),
        required=False,
    )

    policy_relevance = SlateJSONField(
        title=_("Policy / environmental relevance"),
        description=_(
            "The degree to which the indicator meets current/potential needs of users"
        ),
        required=False,
    )

    frequency_of_dissemination = Int(
        title=_("Frequency of dissemination"),
        description=(
            "Time interval at which the indicator is published (in years, from 1 to 5). E.g. use 1 if it is published yearly, 2 if it is published every 2 years and so on."
        ),
        required=False,
        default=1,
        min=1,
        max=10,
    )

    accuracy_and_reliability = SlateJSONField(
        title=_("Accuracy and uncertainties"),
        description=_(
            "Closeness of computations or estimates to the unknown exact or true values that the statistics were intended to measure; closeness of the initial estimated value to the subsequent estimated value. Includes, among others, comparability (geographical and over time)."
        ),
        required=False,
    )

    #
    # Workflow
    #
    model.fieldset(
        "workflow",
        label=_("Workflow"),
        fields=[],
    )


@provider(IFormFieldProvider)
class IIndicatorLayout(model.Schema):
    """IMS Indicator blocks layout"""

    #
    # Layout
    #
    model.fieldset("layout", label=_("Layout"), fields=["blocks", "blocks_layout"])

    blocks = JSONField(
        title=_("Blocks"),
        description=_("The JSON representation of the object blocks."),
        schema=BLOCKS_SCHEMA,
        default={
            "1bc4379d-cddb-4120-84ad-5ab025533b12": {
                "@type": "group",
                "allowedBlocks": ["slate"],
                "as": "section",
                "data": {
                    "blocks": {
                        "6cb82a12-dec8-42ef-9c1c-750fda60b776": {
                            "@type": "slate",
                            "plaintext": "",
                            "value": [{"children": [{"text": ""}], "type": "p"}],
                        },
                        "b0279dde-1ceb-4137-a7f1-5ab7b46a782c": {
                            "@type": "dataFigure",
                            "disableNewBlocks": True,
                            "fixed": True,
                            "instructions": {
                                "content-type": "text/html",
                                "data": "&lt;p&gt;figure instructions goes here&lt;/p&gt;",
                                "encoding": "utf8",
                            },
                            "required": True,
                        },
                        "undefined": {"@type": "slate"},
                    },
                    "blocks_layout": {
                        "items": [
                            "b0279dde-1ceb-4137-a7f1-5ab7b46a782c",
                            "6cb82a12-dec8-42ef-9c1c-750fda60b776",
                        ]
                    },
                },
                "disableInnerButtons": True,
                "disableNewBlocks": False,
                "fixed": True,
                "ignoreSpaces": True,
                "instructions": {
                    "content-type": "text/html",
                    "data": '&lt;p&gt;&lt;strong&gt;Assessment text remains at&lt;/strong&gt; &lt;strong&gt;the relevant&lt;/strong&gt; &lt;strong&gt;aggregate level&lt;/strong&gt; &lt;strong&gt;(i.e.&lt;/strong&gt; &lt;strong&gt;global, EU, sectoral)&lt;/strong&gt; &lt;strong&gt;and addresses the following: &lt;/strong&gt;&lt;/p&gt;&lt;ol keys="dkvn8,e367c,f4lpb,9j981,7ai6k,3g3pd" depth="0"&gt;&lt;li&gt;Explains in one or two sentences on the environmental rationale of the indicator, i.e. why it matters to the environment that we see an increase/decrease in the value measured.&lt;/li&gt;&lt;li&gt;Explains in one or two sentences the associated policy objective, which can be either quantitative or directional. More information on the policy objective and related references will be included in the supporting information section. Where there is no policy objective associated with the indicator, i.e. where the indicator addresses an issue that is important for future policy formulation, this text should explain instead why this issue is important.&lt;/li&gt;&lt;li&gt;IF NECESSARY - Explains any mismatch between what the indicator tracks and what the policy objective/issue is.&lt;/li&gt;&lt;li&gt;Qualifies the historical trend (e.g. steady increase) and explains the key reasons (e.g. policies) behind it. If there is a quantitative target it explains if we are on track to meet it.&lt;/li&gt;&lt;li&gt;IF NECESSARY - Explains any recent changes to the trend and why.&lt;/li&gt;&lt;li&gt;IF NECESSARY - Describes what needs to happen to see adequate progress in future, for instance in order to remain on track to meet targets.&lt;/li&gt;&lt;/ol&gt;&lt;p&gt;&lt;strong&gt;Please cite your work if&lt;/strong&gt; &lt;strong&gt;necessary&lt;/strong&gt; &lt;strong&gt;using the EEA citation style (i.e.&lt;/strong&gt; &lt;strong&gt;EEA, 2020). A full reference list appears in the supporting information section.&lt;/strong&gt;&lt;/p&gt;',
                    "encoding": "utf8",
                },
                "maxChars": "2000",
                "placeholder": "Aggregate level assessment e.g. progress at global, EU level..",
                "readOnlySettings": True,
                "required": True,
                "styles": {},
                "title": "Aggregate level assessment",
                "variation": "default",
            },
            "2dc79b22-b2c8-450a-8044-ef04bfd044cf": {
                "@type": "dividerBlock",
                "disableNewBlocks": True,
                "fixed": True,
                "hidden": True,
                "readOnly": False,
                "required": True,
                "section": False,
                "spacing": "m",
                "styles": {},
            },
            "2ec8ba1c-769d-41fd-98c3-1e72b9c1d736": {
                "@type": "dividerBlock",
                "disableNewBlocks": True,
                "fixed": True,
                "hidden": True,
                "readOnly": False,
                "required": True,
                "section": False,
                "spacing": "m",
                "styles": {},
            },
            "677f7422-6da4-4c86-bca8-de732b7047b9": {
                "@type": "dividerBlock",
                "disableNewBlocks": True,
                "fixed": True,
                "hidden": True,
                "required": True,
                "section": False,
                "spacing": "m",
                "styles": {},
            },
            "794c9b24-5cd4-4b9f-a0cd-b796aadc86e8": {
                "@type": "group",
                "allowedBlocks": [],
                "as": "section",
                "data": {
                    "blocks": {
                        "1c31c956-5086-476a-8694-9936cfa6c240": {
                            "@type": "description",
                            "disableNewBlocks": True,
                            "fixed": True,
                            "instructions": {
                                "content-type": "text/html",
                                "data": "&lt;p&gt;The summary tells the reader about the indicator trend over the examined period and whether or not it helps to achieve the associated policy objective, which can be either quantitative or directional.&lt;/p&gt;&lt;p&gt;In the absence of a policy objective, it explains whether the trend is in the right or wrong direction in relation to the issue examined.&lt;/p&gt;&lt;p&gt;If there has been an important change over the most recent period of the time series, e.g. over the last year, this is indicated too.&lt;/p&gt;&lt;p&gt;Furthermore, if there is a quantitative target, it also indicates whether we are on track to meet it and if not what are the reasons preventing that, e.g. socio-economic drivers, implementation gap etc.&lt;/p&gt;",
                                "encoding": "utf8",
                            },
                            "placeholder": "Summary",
                            "plaintext": "",
                            "required": True,
                            "value": [{"children": [{"text": ""}], "type": "p"}],
                        },
                        "3cccc2bb-471a-44c7-b006-5595c4713ff2": {
                            "@type": "layoutSettings",
                            "disableNewBlocks": True,
                            "fixed": True,
                            "layout_size": "narrow_view",
                            "readOnly": True,
                            "required": True,
                        },
                        "ddde07aa-4e48-4475-94bd-e1a517d26eab": {
                            "@type": "title",
                            "disableNewBlocks": True,
                            "fixed": True,
                            "placeholder": "Indicator title",
                            "required": True,
                        },
                    },
                    "blocks_layout": {
                        "items": [
                            "ddde07aa-4e48-4475-94bd-e1a517d26eab",
                            "1c31c956-5086-476a-8694-9936cfa6c240",
                            "3cccc2bb-471a-44c7-b006-5595c4713ff2",
                        ]
                    },
                },
                "disableInnerButtons": True,
                "disableNewBlocks": True,
                "fixed": True,
                "fixedLayout": True,
                "ignoreSpaces": True,
                "instructions": {
                    "content-type": "text/html",
                    "data": "&lt;p&gt;The summary tells the reader about the indicator trend over the examined period and whether or not it helps to achieve the associated policy objective, which can be either quantitative or directional.&lt;/p&gt;&lt;p&gt;In the absence of a policy objective, it explains whether the trend is in the right or wrong direction in relation to the issue examined.&lt;/p&gt;&lt;p&gt;If there has been an important change over the most recent period of the time series, e.g. over the last year, this is indicated too.&lt;/p&gt;&lt;p&gt;Furthermore, if there is a quantitative target, it also indicates whether we are on track to meet it and if not what are the reasons preventing that, e.g. socio-economic drivers, implementation gap etc.&lt;/p&gt;",
                    "encoding": "utf8",
                },
                "maxChars": "500",
                "readOnlySettings": True,
                "required": True,
                "styles": {"style_name": "environment-theme-bg"},
                "title": "Content header",
            },
            "8cb090c3-7071-40b8-9c7b-aca2ca3d0ad9": {
                "@type": "accordion",
                "allowedBlocks": ["columnsBlock", "slateFootnotes", "metadataSection"],
                "collapsed": True,
                "data": {
                    "blocks": {
                        "309c5ef9-de09-4759-bc02-802370dfa366": {
                            "@type": "accordionPanel",
                            "blocks": {
                                "e047340c-c02e-4247-89ab-5fec73aeb5d3": {
                                    "@type": "columnsBlock",
                                    "data": {
                                        "blocks": {
                                            "a8a2323e-32af-426e-9ede-1f17affd664c": {
                                                "blocks": {
                                                    "fe145094-71e0-4b3d-82f3-e4d79ac13533": {
                                                        "@type": "metadataSection",
                                                        "disableNewBlocks": True,
                                                        "fields": [
                                                            {
                                                                "@id": "94d638f1-89e1-4f97-aa59-b89b565f60fb",
                                                                "field": {
                                                                    "id": "taxonomy_typology",
                                                                    "title": "Typology",
                                                                    "widget": "choices",
                                                                },
                                                                "showLabel": True,
                                                            },
                                                            {
                                                                "@id": "ec261e45-f97d-465c-b5a3-0e4aa5187114",
                                                                "field": {
                                                                    "id": "taxonomy_un_sdgs",
                                                                    "title": "UN SDGs",
                                                                    "widget": "array",
                                                                },
                                                                "showLabel": True,
                                                            },
                                                            {
                                                                "@id": "eaef9ff4-0f8d-4360-9d19-5c6a2fd2dd00",
                                                                "field": {
                                                                    "id": "unit_of_measure",
                                                                    "title": "Unit of measure",
                                                                    "widget": "slate",
                                                                },
                                                                "showLabel": True,
                                                            },
                                                            {
                                                                "@id": "089cd1a1-92d4-47e2-8f6e-4bdb358600fe",
                                                                "field": {
                                                                    "id": "frequency_of_dissemination",
                                                                    "title": "Frequency of dissemination",
                                                                    "widget": "integer",
                                                                },
                                                                "showLabel": True,
                                                            },
                                                        ],
                                                        "fixed": True,
                                                        "fixedLayout": True,
                                                        "readOnly": False,
                                                        "readOnlySettings": True,
                                                        "required": True,
                                                        "title": "Right column",
                                                        "variation": "default",
                                                    }
                                                },
                                                "blocks_layout": {
                                                    "items": [
                                                        "fe145094-71e0-4b3d-82f3-e4d79ac13533"
                                                    ]
                                                },
                                            },
                                            "d9b41958-c17c-45f8-bae1-4140b537a033": {
                                                "blocks": {
                                                    "2a56568a-10af-4a5b-8c73-22aa8cb734fe": {
                                                        "@type": "metadataSection",
                                                        "disableNewBlocks": True,
                                                        "fields": [
                                                            {
                                                                "@id": "48a20e0b-d3bd-41ac-aa06-e97c61071bd2",
                                                                "field": {
                                                                    "id": "taxonomy_dpsir",
                                                                    "title": "DPSIR",
                                                                    "widget": "choices",
                                                                },
                                                                "showLabel": True,
                                                            },
                                                            {
                                                                "@id": "34ceb93f-b405-4afd-aeae-a05abd44d355",
                                                                "field": {
                                                                    "id": "topics",
                                                                    "title": "Topics",
                                                                    "widget": "array",
                                                                },
                                                                "showLabel": True,
                                                            },
                                                            {
                                                                "@id": "fd2cdb9e-5ddd-4b46-8382-0d687ce2883e",
                                                                "field": {
                                                                    "id": "subjects",
                                                                    "title": "Tags",
                                                                    "widget": "tags",
                                                                },
                                                                "showLabel": True,
                                                            },
                                                            {
                                                                "@id": "0e842d87-c9f4-438e-b234-f83141d25ff3",
                                                                "field": {
                                                                    "id": "temporal_coverage",
                                                                    "title": "Temporal coverage",
                                                                    "widget": "temporal",
                                                                },
                                                                "showLabel": True,
                                                            },
                                                            {
                                                                "@id": "0b8ee8c2-046b-4243-9f11-116df6e0a524",
                                                                "field": {
                                                                    "id": "geo_coverage",
                                                                    "title": "Geographic coverage",
                                                                    "widget": "geolocation",
                                                                },
                                                                "showLabel": True,
                                                            },
                                                        ],
                                                        "fixed": True,
                                                        "fixedLayout": True,
                                                        "readOnly": False,
                                                        "readOnlySettings": True,
                                                        "required": True,
                                                        "title": "Left column",
                                                        "variation": "default",
                                                    }
                                                },
                                                "blocks_layout": {
                                                    "items": [
                                                        "2a56568a-10af-4a5b-8c73-22aa8cb734fe"
                                                    ]
                                                },
                                            },
                                        },
                                        "blocks_layout": {
                                            "items": [
                                                "d9b41958-c17c-45f8-bae1-4140b537a033",
                                                "a8a2323e-32af-426e-9ede-1f17affd664c",
                                            ]
                                        },
                                    },
                                    "disableNewBlocks": True,
                                    "fixed": True,
                                    "fixedLayout": True,
                                    "gridCols": ["halfWidth", "halfWidth"],
                                    "gridSize": 12,
                                    "instructions": {
                                        "content-type": "text/html",
                                        "data": "&lt;p&gt;&lt;br/&gt;&lt;/p&gt;",
                                        "encoding": "utf8",
                                    },
                                    "readOnly": False,
                                    "readOnlySettings": True,
                                    "required": True,
                                    "title": "Metadata",
                                }
                            },
                            "blocks_layout": {
                                "items": ["e047340c-c02e-4247-89ab-5fec73aeb5d3"]
                            },
                            "title": "Metadata",
                        },
                        "546a7c35-9188-4d23-94ee-005d97c26f2b": {
                            "@type": "accordionPanel",
                            "blocks": {
                                "b5381428-5cae-4199-9ca8-b2e5fa4677d9": {
                                    "@type": "metadataSection",
                                    "disableNewBlocks": True,
                                    "fields": [
                                        {
                                            "@id": "62c471fc-128f-4eff-98f9-9e83d9643fc7",
                                            "field": {
                                                "id": "data_description",
                                                "title": "Definition",
                                                "widget": "slate",
                                            },
                                            "showLabel": True,
                                        },
                                        {
                                            "@id": "ee67688d-3170-447a-a235-87b4e4ff0928",
                                            "field": {
                                                "id": "methodology",
                                                "title": "Methodology",
                                                "widget": "slate",
                                            },
                                            "showLabel": True,
                                        },
                                        {
                                            "@id": "b8a8f01c-0669-48e3-955d-d5d62da1b555",
                                            "field": {
                                                "id": "policy_relevance",
                                                "title": "Policy/environmental relevance",
                                                "widget": "slate",
                                            },
                                            "showLabel": True,
                                        },
                                        {
                                            "@id": "d71a80d1-0e65-46d9-8bd4-45aca22bc5dc",
                                            "field": {
                                                "id": "accuracy_and_reliability",
                                                "title": "Accuracy and uncertainties",
                                                "widget": "slate",
                                            },
                                            "showLabel": True,
                                        },
                                        {
                                            "@id": "97ed11f5-4d31-4462-b3b0-2756a6880d31",
                                            "field": {
                                                "id": "data_provenance",
                                                "title": "Data sources and providers",
                                                "widget": "data_provenance",
                                            },
                                            "showLabel": True,
                                        },
                                    ],
                                    "fixed": True,
                                    "fixedLayout": True,
                                    "readOnly": False,
                                    "readOnlySettings": True,
                                    "required": True,
                                    "title": "Supporting information",
                                    "variation": "default",
                                }
                            },
                            "blocks_layout": {
                                "items": ["b5381428-5cae-4199-9ca8-b2e5fa4677d9"]
                            },
                            "title": "Supporting information",
                        },
                        "ecdb3bcf-bbe9-4978-b5cf-0b136399d9f8": {
                            "@type": "accordionPanel",
                            "blocks": {
                                "d9aa8ed3-1c8a-4134-a324-663489a04473": {
                                    "@type": "slateFootnotes",
                                    "disableNewBlocks": True,
                                    "fixed": True,
                                    "global": True,
                                    "instructions": {
                                        "content-type": "text/html",
                                        "data": "&lt;p&gt;&lt;br/&gt;&lt;/p&gt;",
                                        "encoding": "utf8",
                                    },
                                    "placeholder": "References and footnotes will appear here",
                                    "readOnlySettings": True,
                                    "required": True,
                                }
                            },
                            "blocks_layout": {
                                "items": ["d9aa8ed3-1c8a-4134-a324-663489a04473"]
                            },
                            "selected": "b142c252-337d-4f6e-8ed2-ff4c43601e2f",
                            "title": "References and footnotes",
                        },
                    },
                    "blocks_layout": {
                        "items": [
                            "546a7c35-9188-4d23-94ee-005d97c26f2b",
                            "309c5ef9-de09-4759-bc02-802370dfa366",
                            "ecdb3bcf-bbe9-4978-b5cf-0b136399d9f8",
                        ]
                    },
                },
                "disableInnerButtons": True,
                "disableNewBlocks": True,
                "fixed": True,
                "fixedLayout": True,
                "instructions": {
                    "content-type": "text/html",
                    "data": "&lt;p&gt;&lt;br/&gt;&lt;/p&gt;",
                    "encoding": "utf8",
                },
                "non_exclusive": False,
                "readOnly": False,
                "readOnlySettings": True,
                "readOnlyTitles": True,
                "required": True,
                "title": "Additional information",
                "title_size": "h3",
            },
            "d060487d-88fc-4f7b-8ea4-003f14e0fb0c": {
                "@type": "group",
                "allowedBlocks": ["slate"],
                "as": "section",
                "data": {
                    "blocks": {
                        "02ba4a04-fcfe-4968-806f-1dac3119cfef": {
                            "@type": "dataFigure",
                            "disableNewBlocks": True,
                            "fixed": True,
                            "instructions": {
                                "content-type": "text/html",
                                "data": "&lt;p&gt;&lt;br/&gt;&lt;/p&gt;",
                                "encoding": "utf8",
                            },
                            "required": True,
                        },
                        "a8410822-a068-42ae-8b4c-6763aec2328d": {
                            "@type": "slate",
                            "plaintext": "",
                            "value": [{"children": [{"text": ""}], "type": "p"}],
                        },
                        "undefined": {
                            "@type": "dividerBlock",
                            "hidden": True,
                            "section": False,
                            "spacing": "s",
                            "styles": {},
                        },
                    },
                    "blocks_layout": {
                        "items": [
                            "02ba4a04-fcfe-4968-806f-1dac3119cfef",
                            "a8410822-a068-42ae-8b4c-6763aec2328d",
                        ]
                    },
                },
                "disableInnerButtons": True,
                "disableNewBlocks": False,
                "fixed": True,
                "ignoreSpaces": True,
                "instructions": {
                    "content-type": "text/html",
                    "data": '&lt;ol keys="9bbul,b1sa2,171og,1c1t5" depth="0"&gt;&lt;li&gt;Depending on the indicator context, this text can provide information at country level or, if this is not relevant, at some other level, e.g. sectoral, regional level.&lt;/li&gt;&lt;li&gt;This text interprets the data represented in the chart, rather than describing results, i.e. it provides explanations for some of the results.&lt;/li&gt;&lt;li&gt;The text related to progress at this level does not have to be comprehensive.&lt;/li&gt;&lt;li&gt;If there is no information that adds value to what is already visible there is no need to have any text.&lt;/li&gt;&lt;/ol&gt;',
                    "encoding": "utf8",
                },
                "maxChars": "1000",
                "placeholder": "Disaggregate level assessment e.g. country, sectoral, regional level assessment",
                "readOnly": False,
                "readOnlySettings": True,
                "required": True,
                "styles": {},
                "title": "Disaggregate level assessment",
                "variation": "default",
            },
            "e9736b7c-4902-48aa-aecd-b706409a576d": {
                "@type": "dividerBlock",
                "disableNewBlocks": True,
                "fixed": True,
                "hidden": True,
                "required": True,
                "section": False,
                "spacing": "m",
                "styles": {},
            },
            "undefined": {
                "as": "section",
                "@type": "group",
                "allowedBlocks": ["slate", "dividerBlock"],
                "data": {
                    "blocks": {
                        "6cb82a12-dec8-42ef-9c1c-750fda60b776": {
                            "@type": "slate",
                            "plaintext": "",
                            "value": [{"children": [{"text": ""}], "type": "p"}],
                        },
                        "b0279dde-1ceb-4137-a7f1-5ab7b46a782c": {
                            "@type": "dataFigure",
                            "disableNewBlocks": True,
                            "fixed": True,
                            "instructions": {
                                "content-type": "text/html",
                                "data": "&lt;p&gt;figure instructions goes here&lt;/p&gt;",
                                "encoding": "utf8",
                            },
                            "required": True,
                        },
                        "undefined": {"@type": "slate"},
                    },
                    "blocks_layout": {
                        "items": [
                            "b0279dde-1ceb-4137-a7f1-5ab7b46a782c",
                            "6cb82a12-dec8-42ef-9c1c-750fda60b776",
                        ]
                    },
                },
                "disableInnerButtons": True,
                "disableNewBlocks": False,
                "fixed": True,
                "ignoreSpaces": True,
                "instructions": {
                    "content-type": "text/html",
                    "data": '&lt;p&gt;&lt;strong&gt;Assessment text remains at&lt;/strong&gt; &lt;strong&gt;the relevant&lt;/strong&gt; &lt;strong&gt;aggregate level&lt;/strong&gt; &lt;strong&gt;(i.e.&lt;/strong&gt; &lt;strong&gt;global, EU, sectoral)&lt;/strong&gt; &lt;strong&gt;and addresses the following: &lt;/strong&gt;&lt;/p&gt;&lt;ol keys="dkvn8,e367c,f4lpb,9j981,7ai6k,3g3pd" depth="0"&gt;&lt;li&gt;Explains in one or two sentences on the environmental rationale of the indicator, i.e. why it matters to the environment that we see an increase/decrease in the value measured.&lt;/li&gt;&lt;li&gt;Explains in one or two sentences the associated policy objective, which can be either quantitative or directional. More information on the policy objective and related references will be included in the supporting information section. Where there is no policy objective associated with the indicator, i.e. where the indicator addresses an issue that is important for future policy formulation, this text should explain instead why this issue is important.&lt;/li&gt;&lt;li&gt;IF NECESSARY - Explains any mismatch between what the indicator tracks and what the policy objective/issue is.&lt;/li&gt;&lt;li&gt;Qualifies the historical trend (e.g. steady increase) and explains the key reasons (e.g. policies) behind it. If there is a quantitative target it explains if we are on track to meet it.&lt;/li&gt;&lt;li&gt;IF NECESSARY - Explains any recent changes to the trend and why.&lt;/li&gt;&lt;li&gt;IF NECESSARY - Describes what needs to happen to see adequate progress in future, for instance in order to remain on track to meet targets.&lt;/li&gt;&lt;/ol&gt;&lt;p&gt;&lt;strong&gt;Please cite your work if&lt;/strong&gt; &lt;strong&gt;necessary&lt;/strong&gt; &lt;strong&gt;using the EEA citation style (i.e.&lt;/strong&gt; &lt;strong&gt;EEA, 2020). A full reference list appears in the supporting information section.&lt;/strong&gt;&lt;/p&gt;',
                    "encoding": "utf8",
                },
                "maxChars": "2000",
                "placeholder": "Aggregate level assessment e.g. progress at global, EU level..",
                "readOnlySettings": True,
                "required": True,
                "styles": {},
                "title": "Aggregate level assessment",
                "variation": "default",
            },
        },
        required=False,
    )

    blocks_layout = JSONField(
        title=_("Blocks Layout"),
        description=_("The JSON representation of the object blocks layout."),
        schema=LAYOUT_SCHEMA,
        default={
            "items": [
                "794c9b24-5cd4-4b9f-a0cd-b796aadc86e8",
                "2dc79b22-b2c8-450a-8044-ef04bfd044cf",
                "1bc4379d-cddb-4120-84ad-5ab025533b12",
                "677f7422-6da4-4c86-bca8-de732b7047b9",
                "d060487d-88fc-4f7b-8ea4-003f14e0fb0c",
                "e9736b7c-4902-48aa-aecd-b706409a576d",
                "8cb090c3-7071-40b8-9c7b-aca2ca3d0ad9",
                "2ec8ba1c-769d-41fd-98c3-1e72b9c1d736",
            ]
        },
        required=False,
    )
