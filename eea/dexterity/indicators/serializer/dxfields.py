"""dxfields serializers and deserializers"""

from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import ISerializeToJson, IDeserializeFromJson
from plone.restapi.serializer.dxcontent import SerializeToJson
from plone.restapi.deserializer.dxcontent import DeserializeFromJson
from plone.restapi.serializer.utils import uid_to_url
from plone.restapi.deserializer.utils import path2uid
from plone.app.uuid.utils import uuidToCatalogBrain
from eea.dexterity.indicators.interfaces import IIndicator


@implementer(ISerializeToJson)
@adapter(IIndicator, IBrowserRequest)
class IndicatorSerializer(SerializeToJson):
    """Custom serializer for Indicator to convert UUID to URLs for copied_from/copied_to"""

    def __call__(self, version=None, include_items=True):
        result = super().__call__(version=version, include_items=include_items)

        # Convert copied_from UUID to URL
        if "copied_from" in result and result["copied_from"]:
            uid = result["copied_from"]
            brain = uuidToCatalogBrain(uid)
            if brain:
                result["copied_from"] = brain.getURL()
            else:
                result["copied_from"] = uid_to_url(f"resolveuid/{uid}")

        # Convert copied_to UUID to URL
        if "copied_to" in result and result["copied_to"]:
            uid = result["copied_to"]
            brain = uuidToCatalogBrain(uid)
            if brain:
                result["copied_to"] = brain.getURL()
            else:
                result["copied_to"] = uid_to_url(f"resolveuid/{uid}")

        return result


@implementer(IDeserializeFromJson)
@adapter(IIndicator, IBrowserRequest)
class IndicatorDeserializer(DeserializeFromJson):
    """Custom deserializer for Indicator to convert URLs back to UUIDs for copied_from/copied_to"""

    def __call__(self, validate_all=False, create=False):
        # Get the data before processing
        data = self.request.get("BODY", {})
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        if isinstance(data, str):
            import json

            try:
                data = json.loads(data)
            except (ValueError, TypeError):
                data = {}

        # Convert copied_from URL back to UUID
        if "copied_from" in data and data["copied_from"]:
            data["copied_from"] = path2uid(
                context=self.context, link=data["copied_from"]
            )

        # Convert copied_to URL back to UUID
        if "copied_to" in data and data["copied_to"]:
            data["copied_to"] = path2uid(context=self.context, link=data["copied_to"])

        # Continue with normal deserialization
        return super().__call__(validate_all=validate_all, create=create)
