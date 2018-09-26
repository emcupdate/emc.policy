##############################################################################
#
# Copyright (c) 2011 Zope Foundation and Contributors
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this
# distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import unittest
from Products.PluggableAuthService.interfaces.events import \
    IPrincipalDeletedEvent
from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin
from zope.component import adapter
from zope.component import getGlobalSiteManager
from plone.app.testing.bbb import PloneTestCase as TestCase
from emc.policy.testing import INTEGRATION_TESTING

class ConformsToIPASEvent:

    def test_class_conforms_to_IPASEvent(self):
        from zope.interface.verify import verifyClass
        from Products.PluggableAuthService.interfaces.events import IPASEvent
        verifyClass(IPASEvent, self._getTargetClass())

    def test_instance_conforms_to_IPASEvent(self):
        from zope.interface.verify import verifyObject
        from Products.PluggableAuthService.interfaces.events import IPASEvent
        verifyObject(IPASEvent, self._makeOne())


class PASEventTests(unittest.TestCase, ConformsToIPASEvent):

    def _getTargetClass(self):
        from Products.PluggableAuthService.events import PASEvent
        return PASEvent

    def _makeOne(self, principal=None):
        if principal is None:
            principal = DummyPrincipal()
        return self._getTargetClass()(principal)


class PrincipalCreatedTests(unittest.TestCase, ConformsToIPASEvent):

    def _getTargetClass(self):
        from Products.PluggableAuthService.events import PrincipalCreated
        return PrincipalCreated

    def _makeOne(self, principal=None):
        if principal is None:
            principal = DummyPrincipal()
        return self._getTargetClass()(principal)

    def test_class_conforms_to_IPrincipalCreatedEvent(self):
        from zope.interface.verify import verifyClass
        from Products.PluggableAuthService.interfaces.events \
            import IPrincipalCreatedEvent
        verifyClass(IPrincipalCreatedEvent, self._getTargetClass())

    def test_instance_conforms_to_IPrincipalCreatedEvent(self):
        from zope.interface.verify import verifyObject
        from Products.PluggableAuthService.interfaces.events \
            import IPrincipalCreatedEvent
        verifyObject(IPrincipalCreatedEvent, self._makeOne())


class PrincipalDeletedTests(TestCase, ConformsToIPASEvent):

    layer = INTEGRATION_TESTING    
    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.acl_users = self.portal.acl_users
        

    def createUser(self, login="created_user", password="secret",
                   roles=[], groups=[], domains=()):
        self.acl_users.userFolderAddUser(
            login, password, roles=roles, groups=groups, domains=domains,)

            
    def _getTargetClass(self):
        from Products.PluggableAuthService.events import PrincipalDeleted
        return PrincipalDeleted

    def _makeOne(self, principal=None):
        if principal is None:
            principal = DummyPrincipal()
        return self._getTargetClass()(principal)

    def test_class_conforms_to_IPrincipalDeletedEvent(self):
        from zope.interface.verify import verifyClass
        from Products.PluggableAuthService.interfaces.events \
            import IPrincipalDeletedEvent
        verifyClass(IPrincipalDeletedEvent, self._getTargetClass())

    def test_instance_conforms_to_IPrincipalDeletedEvent(self):
        from zope.interface.verify import verifyObject
        from Products.PluggableAuthService.interfaces.events \
            import IPrincipalDeletedEvent
        verifyObject(IPrincipalDeletedEvent, self._makeOne())
    
    def test_principal_del_event(self):
        eventsFired = []

        @adapter(IPrincipalDeletedEvent)
        def gotDeletion(event):

            eventsFired.append(event)

        gsm = getGlobalSiteManager()
        gsm.registerHandler(gotDeletion)
        self.createUser()
        self.acl_users.userFolderDelUsers(['created_user'])
        self.assertEqual(len(eventsFired), 1)
        self.assertEqual(eventsFired[0].principal, 'created_user')
        gsm.unregisterHandler(gotDeletion)

class CredentialsUpdatedTests(unittest.TestCase, ConformsToIPASEvent):

    def _getTargetClass(self):
        from Products.PluggableAuthService.events import CredentialsUpdated
        return CredentialsUpdated

    def _makeOne(self, principal=None, password='password'):
        if principal is None:
            principal = DummyPrincipal()
        return self._getTargetClass()(principal, password)

    def test_class_conforms_to_ICredentialsUpdatedEvent(self):
        from zope.interface.verify import verifyClass
        from Products.PluggableAuthService.interfaces.events \
            import ICredentialsUpdatedEvent
        verifyClass(ICredentialsUpdatedEvent, self._getTargetClass())

    def test_instance_conforms_to_ICredentialsUpdatedEvent(self):
        from zope.interface.verify import verifyObject
        from Products.PluggableAuthService.interfaces.events \
            import ICredentialsUpdatedEvent
        verifyObject(ICredentialsUpdatedEvent, self._makeOne())


class PropertiesUpdatedTests(unittest.TestCase, ConformsToIPASEvent):

    def _getTargetClass(self):
        from Products.PluggableAuthService.events import PropertiesUpdated
        return PropertiesUpdated

    def _makeOne(self, principal=None, properties=None):
        if principal is None:
            principal = DummyPrincipal()
        if properties is None:
            properties = {}
        return self._getTargetClass()(principal, properties)

    def test_class_conforms_to_IPropertiesUpdatedEvent(self):
        from zope.interface.verify import verifyClass
        from Products.PluggableAuthService.interfaces.events \
            import IPropertiesUpdatedEvent
        verifyClass(IPropertiesUpdatedEvent, self._getTargetClass())

    def test_instance_conforms_to_IPropertiesUpdatedEvent(self):
        from zope.interface.verify import verifyObject
        from Products.PluggableAuthService.interfaces.events \
            import IPropertiesUpdatedEvent
        verifyObject(IPropertiesUpdatedEvent, self._makeOne())


class DummyPrincipal(object):
    pass


class GroupDeletedTests(unittest.TestCase, ConformsToIPASEvent):

    def _getTargetClass(self):
        from Products.PluggableAuthService.events import GroupDeleted
        return GroupDeleted

    def _makeOne(self, Group=None):
        if Group is None:
            Group = DummyGroup()
        return self._getTargetClass()(Group)

    def test_class_conforms_to_IGroupDeletedEvent(self):
        from zope.interface.verify import verifyClass
        from Products.PluggableAuthService.interfaces.events \
            import IGroupDeletedEvent
        verifyClass(IGroupDeletedEvent, self._getTargetClass())

    def test_instance_conforms_to_IGroupDeletedEvent(self):
        from zope.interface.verify import verifyObject
        from Products.PluggableAuthService.interfaces.events \
            import IGroupDeletedEvent
        verifyObject(IGroupDeletedEvent, self._makeOne())


class DummyGroup(object):
    pass

