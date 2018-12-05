import logging
from cStringIO import StringIO

import transaction
from zope import event
from zope.interface import implements

from DateTime import DateTime
from App.class_init import InitializeClass
from App.special_dtml import DTMLFile
from OFS.Image import Image

from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from AccessControl.requestmethod import postonly
from Acquisition import aq_get
from Acquisition import aq_inner
from Acquisition import aq_parent
from zExceptions import BadRequest
from ZODB.POSException import ConflictError

from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.permissions import ManageUsers
from Products.CMFCore.permissions import SetOwnProperties
from Products.CMFCore.permissions import SetOwnPassword
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.MembershipTool import MembershipTool as BaseTool

from Products.PlonePAS.events import UserLoggedInEvent
from Products.PlonePAS.events import UserInitialLoginInEvent
from Products.PlonePAS.events import UserLoggedOutEvent
from emc.policy.events import AddloginEvent,NormalUserloginEvent
from Products.PlonePAS.interfaces import membership
from Products.PlonePAS.utils import cleanId
from Products.PlonePAS.utils import scale_image
from emc.policy import get_ip,fmt,list2str,getfullname_orid
import datetime

default_portrait = 'defaultUser.png'
logger = logging.getLogger('PlonePAS')
memberareaCreationFlag = True

from emc.memberArea.events import MemberAreaCreatedEvent


def get_enable_user_folders(self):
    return True
#    security.declarePublic('createMemberarea')
def loginUser(self, REQUEST=None):
        """ Handle a login for the current user.

        This method takes care of all the standard work that needs to be
        done when a user logs in:
        - clear the copy/cut/paste clipboard
        - PAS credentials update
        - sending a logged-in event
        - storing the login time
        - create the member area if it does not exist
        """
        user=getSecurityManager().getUser()
        if user is None:
            return
        try:
            home = self.getHomeFolder(user.getId())
        except:
            home = None
        res = self.setLoginTimes()
        res = res and not home
        
        loginEvent = NormalUserloginEvent(userid = getfullname_orid(user),
                                     datetime = datetime.datetime.now().strftime(fmt),
                                     ip = get_ip(),
                                     type = 0,
                                     description = "",
                                     result = 1)
        if loginEvent.available():
            if loginEvent.is_normal_user():
                event.notify(loginEvent)
            else:
                loginEvent = AddloginEvent(adminid = getfullname_orid(user),
                                     userid = " ",
                                     datetime = datetime.datetime.now().strftime(fmt),
                                     ip = get_ip(),
                                     type = 0,
                                     description = "",
                                     result = 1)                
                event.notify(loginEvent)
        if res:
            event.notify(UserInitialLoginInEvent(user))
            self.createMemberArea()
            event.notify(MemberAreaCreatedEvent(user))                        
        else:
            event.notify(UserLoggedInEvent(user))

        if REQUEST is None:
            REQUEST=getattr(self, 'REQUEST', None)
        if REQUEST is None:
            return

        # Expire the clipboard
        if REQUEST.get('__cp', None) is not None:
            REQUEST.RESPONSE.expireCookie('__cp', path='/')


        try:
            pas = getToolByName(self, 'acl_users')
            
            pas.credentials_cookie_auth.login()


        except AttributeError:
            # The cookie plugin may not be present
            pass

