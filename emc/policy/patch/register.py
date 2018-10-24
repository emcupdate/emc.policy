# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.interfaces import ISecuritySchema
from Products.CMFPlone.utils import normalizeString
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from ZODB.POSException import ConflictError
from plone.autoform.form import AutoExtensibleForm
from plone.autoform.interfaces import OMITTED_KEY
from plone.protect import CheckAuthenticator
from plone.registry.interfaces import IRegistry
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.interfaces import DISPLAY_MODE
from zExceptions import Forbidden
from zope.component import (
    getUtility,
    queryUtility,
    getAdapter,
    provideAdapter,
    getMultiAdapter)
from zope.component.hooks import getSite
from zope.schema import getFieldNames
import logging

from plone.app.users.schema import (
    IRegisterSchema,
    IAddUserSchema,
    ICombinedRegisterSchema
)
from plone.app.users.utils import (
    notifyWidgetActionExecutionError,
    uuid_userid_generator,
)
from plone.app.users.browser.register import AddUserForm
from plone.app.users.browser.account import AccountPanelSchemaAdapter
from plone.app.users.browser.schemaeditor import getFromBaseSchema

from plone.app.users.browser.interfaces import ILoginNameGenerator
from plone.app.users.browser.interfaces import IUserIdGenerator

# Number of retries for creating a user id like bob-jones-42:
RENAME_AFTER_CREATION_ATTEMPTS = 100


def getRegisterSchema():
    portal = getSite()
    schema = getattr(portal, '_v_register_schema', None)
    if schema is None:
        portal._v_register_schema = schema = getFromBaseSchema(
            ICombinedRegisterSchema,
            form_name=u'On Registration'
        )
        # as schema is a generated supermodel,
        # needed adapters can only be registered at run time
        provideAdapter(AccountPanelSchemaAdapter, (IPloneSiteRoot,), schema)
    return schema

def updateFields(self):
        super(AddUserForm, self).updateFields()
        defaultFields = field.Fields(self.fields)

        # The mail_me field needs special handling depending on the
        # enable_user_pwd_choice setting and on the correctness of the mail
        # settings.
        portal = getUtility(ISiteRoot)
        ctrlOverview = getMultiAdapter((portal, self.request),
                                       name='overview-controlpanel')
        mail_settings_correct = not ctrlOverview.mailhost_warning()
        if mail_settings_correct:
            # Make the password fields optional: either specify a
            # password or mail the user (or both).  The validation
            # will check that at least one of the options is chosen.
            defaultFields['password'].field.required = False
            defaultFields['password_ctl'].field.required = False
            settings = self._get_security_settings()
            if not settings.enable_user_pwd_choice:
                defaultFields['mail_me'].field.default = True
            else:
                defaultFields['mail_me'].field.default = False

        # Append the manager-focused fields
        self.fields = defaultFields
