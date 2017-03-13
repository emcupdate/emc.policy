import unittest as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import login
from plone.app.testing import logout

from emc.policy.testing import INTEGRATION_TESTING

from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from Products.CMFCore.utils import getToolByName

from emc.policy.portlets import navigation

class TestPortlet(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='emc.portlets.Navigation')
        self.assertEquals(portlet.addview, 'emc.portlets.Navigation')

    def testInterfaces(self):
        portlet = navigation.Assignment()
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portal = self.layer['portal']
        
        portlet = getUtility(IPortletType, name='emc.portlets.Navigation')
        mapping = portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        
#         for m in mapping.keys():
#             del mapping[m]
#         
# 
#         addview = mapping.restrictedTraverse('+/' + portlet.addview)
# 
#         addview()
# 
        self.assertEquals(len(mapping), 2)
        self.assertTrue(isinstance(mapping.values()[1], navigation.Assignment))

    def testRenderer(self):
        context = self.layer['portal']
        request = self.layer['request']
        
        view = context.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=context)
        assignment = navigation.Assignment()

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.assertTrue(isinstance(renderer, navigation.Renderer))

class TestRenderer(unittest.TestCase):
     
    layer = INTEGRATION_TESTING
     
    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
         
        setRoles(portal, TEST_USER_ID, ('Manager',))
         
        membership = getToolByName(portal, 'portal_membership')
        membership.addMember('member1', 'secret', ('Manager',), ())
        membership.addMember('member2', 'secret', ('Member',), ())        
        portal.invokeFactory('emc.project.projectFolder', 'folder1')
        portal['folder1'].invokeFactory('emc.project.project', 'project1')  
        portal['folder1']['project1'].invokeFactory('emc.project.team', 'team1')
        portal['folder1']['project1'].invokeFactory('emc.project.team2', 'team2')        
        portal['folder1']['project1']['team1'].invokeFactory('emc.project.doc', 'audit1')
        portal['folder1']['project1']['team1'].invokeFactory('emc.project.making', 'making1') 
         
        self.membership = getToolByName(portal, 'portal_membership')
         
        setRoles(portal, TEST_USER_ID, ('Member',))
     
    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        portal = self.layer['portal']
         
        context = context or portal
        request = request or self.layer['request']
         
        view = view or portal.restrictedTraverse('@@plone')
         
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=portal)
        assignment = assignment or navigation.Assignment()
 
        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
     
    def test_anonymous(self):
        portal = self.layer['portal']
         
        member = self.membership.getAuthenticatedMember()        
        logout()         
        r = self.renderer(context=portal, assignment=navigation.Assignment())
        self.assertFalse(r.available)
 
    def test_no_project(self):
        portal = self.layer['portal']
         
        login(portal, "member1")
        member = self.membership.getAuthenticatedMember()

        r = self.renderer(context=portal, assignment=navigation.Assignment(topLevel=0))
        self.assertTrue(r.available)
        logout()
        login(portal, "member2")
        import pdb
        pdb.set_trace()        
        r = self.renderer(context=portal, assignment=navigation.Assignment(topLevel=0))
        self.assertFalse(r.available)        
#         self.assertEqual(len(list(r.cinemas())), 0)
         
    def test_single(self):
        portal = self.layer['portal']
         
        member = self.membership.getAuthenticatedMember()

        r = self.renderer(context=portal, assignment=navigation.Assignment())
        self.assertTrue(r.available)
        cinemaUrls = [c['url'] for c in r.cinemas()]
        self.assertEqual(len(cinemaUrls), 1)
        self.assertEqual(cinemaUrls[0], portal.cinemas.c1.absolute_url())
 
    def test_multiple(self):
        portal = self.layer['portal']
         
        member = self.membership.getAuthenticatedMember()
        member.setProperties(homeCinemas=['C1', 'C2'])
        r = self.renderer(context=portal, assignment=navigation.Assignment())
        self.assertTrue(r.available)
        cinemaUrls = [c['url'] for c in r.cinemas()]
        self.assertEqual(len(cinemaUrls), 2)
        self.assertEqual(cinemaUrls[0], portal.cinemas.c1.absolute_url())
        self.assertEqual(cinemaUrls[1], portal.cinemas.c2.absolute_url())
