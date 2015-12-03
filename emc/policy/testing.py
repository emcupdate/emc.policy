#-*- coding: UTF-8 -*-
import datetime
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting,FunctionalTesting

from plone.app.testing import (
IntegrationTesting,
FunctionalTesting,
login, logout, setRoles,
PLONE_FIXTURE,
TEST_USER_NAME,
SITE_OWNER_NAME,
)

from plone.testing import z2
from plone.namedfile.file import NamedImage
from plone import namedfile
from zope.configuration import xmlconfig

def getFile(filename):
    """ return contents of the file with the given name """
    import os
    filename = os.path.join(os.path.dirname(__file__) + "/tests/", filename)
    return open(filename, 'r')

class SitePolicy(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import emc.policy
        import emc.theme
        import emc.bokeh
        xmlconfig.file('configure.zcml', emc.policy, context=configurationContext)
        xmlconfig.file('configure.zcml', emc.theme, context=configurationContext)
        xmlconfig.file('configure.zcml', emc.bokeh, context=configurationContext)
     
        # Install products that use an old-style initialize() function

       
    
    def tearDownZope(self, app):
        # Uninstall products installed above
        pass

     
        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'emc.policy:default')
        applyProfile(portal, 'emc.theme:default')
        applyProfile(portal, 'emc.bokeh:default')


class IntegrationSitePolicy(SitePolicy):      
        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'emc.policy:default')
        applyProfile(portal, 'emc.theme:default')
        applyProfile(portal, 'emc.bokeh:default')
#        portal = self.layer['portal']
        #make global request work
        from zope.globalrequest import setRequest
        setRequest(portal.REQUEST)
        # login doesn't work so we need to call z2.login directly
        z2.login(portal.__parent__.acl_users, SITE_OWNER_NAME)
#        setRoles(portal, TEST_USER_ID, ('Manager',))
#        login(portal, TEST_USER_NAME)
#        portal.invokeFactory('dexterity.membrane.memberfolder', 'memberfolder1')
#           # 社团经手人账号     
#     
#
#        data = getFile('demo.txt').read()
#        item = portal['orgnizationfolder1']['orgnization1']['survey1']
#        item.image = NamedImage(data, 'image/gif', u'image.gif')
#        item.report = namedfile.NamedBlobFile(data,filename=u"demo.txt")               
        self.portal = portal 

POLICY_FIXTURE = SitePolicy()
INTEGRATION_FIXTURE = IntegrationSitePolicy()
INTEGRATION_TESTING = IntegrationTesting(bases=(INTEGRATION_FIXTURE,), name="Site:Integration")
FunctionalTesting = FunctionalTesting(bases=(POLICY_FIXTURE,), name="Site:FunctionalTesting")