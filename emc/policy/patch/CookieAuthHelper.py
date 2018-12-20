##############################################################################
#
# Copyright (c) 2001 Zope Foundation and Contributors
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
""" Class: CookieAuthHelper

$Id$
"""

from base64 import encodestring, decodestring
from binascii import Error
from urllib import quote, unquote

from AccessControl.SecurityInfo import ClassSecurityInfo
from AccessControl.Permissions import view
from OFS.Folder import Folder
from App.class_init import default__class_init__ as InitializeClass

from zope.interface import Interface

from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate

from Products.PluggableAuthService.interfaces.plugins import \
        ILoginPasswordHostExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import \
        IChallengePlugin
from Products.PluggableAuthService.interfaces.plugins import \
        ICredentialsUpdatePlugin
from Products.PluggableAuthService.interfaces.plugins import \
        ICredentialsResetPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from plone import api



def unauthorized(self):
        req = self.REQUEST
        resp = req['RESPONSE']

        # If we set the auth cookie before, delete it now.
        if resp.cookies.has_key(self.cookie_name):
            del resp.cookies[self.cookie_name]

        # Redirect if desired.

        url = "%s/@@auth-tips" % api.portal.get().absolute_url()
        if url is not None: 
            resp.redirect(url, lock=1)
            return 1

        # Could not challenge.
        return 0




