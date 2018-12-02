from AccessControl import ClassSecurityInfo, Unauthorized
from AccessControl import getSecurityManager
from AccessControl.requestmethod import postonly
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from Acquisition import aq_base, aq_chain
from App.class_init import InitializeClass
from email import message_from_string
from hashlib import md5
from plone.registry.interfaces import IRegistry
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.permissions import AddPortalMember
from Products.CMFCore.RegistrationTool import RegistrationTool as BaseTool
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import ISecuritySchema
from Products.CMFPlone.permissions import ManagePortal
from Products.CMFPlone.PloneBaseTool import PloneBaseTool
from Products.CMFPlone.PloneTool import EMAIL_RE
from Products.PluggableAuthService.interfaces.authservice import IPluggableAuthService
from Products.PluggableAuthService.interfaces.plugins import IValidationPlugin
from Products.PluggableAuthService.permissions import SetOwnPassword
from smtplib import SMTPException, SMTPRecipientsRefused
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from zope.schema import ValidationError
import random
import re



def isMemberIdAllowed(self, id):
        if len(id) < 1 or id == 'Anonymous User':
            return 0
#         if not self._ALLOWED_MEMBER_ID_PATTERN.match(id):
#             return 0

        pas = getToolByName(self, 'acl_users')
        if IPluggableAuthService.providedBy(pas):
            results = pas.searchPrincipals(id=id, exact_match=True)
            if results:
                return 0
            else:
                for parent in aq_chain(self):
                    if hasattr(aq_base(parent), "acl_users"):
                        parent = parent.acl_users
                        if IPluggableAuthService.providedBy(parent):
                            if parent.searchPrincipals(id=id,
                                                       exact_match=True):
                                return 0
            # When email addresses are used as logins, we need to check
            # if there are any users with the requested login.
            registry = getUtility(IRegistry)
            security_settings = registry.forInterface(
                ISecuritySchema, prefix='plone')

            if security_settings.use_email_as_login:
                results = pas.searchUsers(name=id, exact_match=True)
                if results:
                    return 0
        else:
            membership = getToolByName(self, 'portal_membership')
            if membership.getMemberById(id) is not None:
                return 0
            groups = getToolByName(self, 'portal_groups')
            if groups.getGroupById(id) is not None:
                return 0

        return 1

