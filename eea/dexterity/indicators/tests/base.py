""" Base test cases
"""
from plone.app.testing import (
    TEST_USER_ID,
    FunctionalTesting,
    PloneSandboxLayer,
    applyProfile,
    setRoles,
)
from plone.testing import z2
from Products.CMFPlone import setuphandlers


class EEAFixture(PloneSandboxLayer):
    """EEA Testing Policy"""

    def setUpZope(self, app, configurationContext):
        """Setup Zope"""
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import eea.api.layout

        self.loadZCML(package=eea.api.layout)
        import eea.schema.slate

        self.loadZCML(package=eea.schema.slate)
        import eea.dexterity.indicators

        self.loadZCML(package=eea.dexterity.indicators)
        z2.installProduct(app, "eea.dexterity.indicators")

    def setUpPloneSite(self, portal):
        """Setup Plone"""
        applyProfile(portal, "eea.dexterity.indicators:default")

        # Default workflow
        wftool = portal["portal_workflow"]
        wftool.setDefaultChain("simple_publication_workflow")

        # Login as manager
        setRoles(portal, TEST_USER_ID, ["Manager"])

        # Add default Plone content
        try:
            applyProfile(portal, "plone.app.contenttypes:plone-content")
        except KeyError:
            # BBB Plone 4
            setuphandlers.setupPortalContent(portal)

        # Create testing environment
        portal.invokeFactory("Folder", "sandbox", title="Sandbox")

    def tearDownZope(self, app):
        """Uninstall Zope"""
        z2.uninstallProduct(app, "eea.dexterity.indicators")


EEAFIXTURE = EEAFixture()
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EEAFIXTURE,), name="EEAindicators:Functional"
)
