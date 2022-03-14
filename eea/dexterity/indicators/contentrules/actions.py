""" EEAContentTypes actions for plone.app.contentrules
"""

import logging
from datetime import datetime

from DateTime import DateTime
from OFS.SimpleItem import SimpleItem
from plone import api
from z3c.form import form
from plone.app.contentrules.browser.formhelper import AddForm, EditForm
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from zope.component import adapter
from zope.interface import Interface, implementer

logger = logging.getLogger("eea.dexterity.indicators")


class IRetractAndRenameOldVersionAction(Interface):
    """ Retract and rename old version
    """


@implementer(IRetractAndRenameOldVersionAction, IRuleElementData)
class RetractAndRenameOldVersionAction(SimpleItem):
    """ Retract and rename old version action
    """

    element = 'eea.dexterity.indicators.retract_and_rename_old_version'
    action = None

    def summary(self):
        """ Summary
        """
        return (
            "Will retract, rename older version of an Indicator. "
            "Then rename current one."
        )


@implementer(IExecutable)
@adapter(Interface, IRetractAndRenameOldVersionAction, Interface)
class RetractAndRenameOldVersionExecutor(object):
    """ Retract and rename old version executor
    """
    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        obj = self.event.object
        oid = obj.getId()
        if not oid.startswith('copy_of_'):
            return True

        parent = obj.getParentNode()
        old_id = oid.replace('copy_of_', '', 1)
        new_id = old_id + '-%s' % datetime.now().timestamp()

        try:
            old_version = parent[old_id]
            api.content.transition(
                obj=old_version, transition='markForDeletion')
            api.content.rename(obj=old_version, new_id=new_id)
            api.content.rename(obj=obj, new_id=old_id)
            obj.setEffectiveDate(DateTime())
        except Exception as err:
            logger.exception(err)
            return True
        return True


class RetractAndRenameOldVersionAddForm(AddForm):
    """ Retract and rename old version addform
    """
    schema = IRetractAndRenameOldVersionAction
    label = u"Retract and rename old version Action"
    description = u"Retract and rename old version action."
    form_name = u"Configure element"
    Type = RetractAndRenameOldVersionAction

    def create(self, data):
        """
        Since content rules expects paths, we're transforming UUID, which
        is what the z3c form widget uses, to paths.
        """
        a = self.Type()
        form.applyChanges(self, a, data)
        return a


class RetractAndRenameOldVersionEditForm(EditForm):
    """ Retract and rename old version editform
    """
    schema = IRetractAndRenameOldVersionAction
    label = u"Retract and rename old version Action"
    description = u"Retract and rename old version action."
    form_name = u"Configure element"
