
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('emc.policy')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
# pas alterations and monkies  
# here patch for Products.PlonePAS.pas
from AccessControl import Unauthorized
from AccessControl import getSecurityManager
from AccessControl.PermissionRole import PermissionRole
from AccessControl.Permissions import change_permissions
from AccessControl.Permissions import manage_properties
from AccessControl.Permissions import manage_users as ManageUsers
from AccessControl.requestmethod import postonly
from OFS.Folder import Folder
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import registerToolInterface
from Products.PlonePAS.interfaces.group import IGroupIntrospection
from Products.PlonePAS.interfaces.group import IGroupManagement
from Products.PlonePAS.interfaces.plugins import ILocalRolesPlugin
from Products.PlonePAS.interfaces.plugins import IUserIntrospection
from Products.PlonePAS.interfaces.plugins import IUserManagement
from Products.PlonePAS.patch import ORIG_NAME
from Products.PlonePAS.patch import wrap_method
from Products.PluggableAuthService.PluggableAuthService import \
    PluggableAuthService
from Products.PluggableAuthService.PluggableAuthService import \
    _SWALLOWABLE_PLUGIN_EXCEPTIONS
from Products.PluggableAuthService.events import PrincipalDeleted
from emc.policy.events import DeleteMemberEvent
from Products.PluggableAuthService.interfaces.authservice import \
    IPluggableAuthService
from Products.PluggableAuthService.interfaces.plugins import \
    IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import \
    IGroupEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins import \
    IRoleAssignerPlugin
from Products.PluggableAuthService.interfaces.plugins import \
    IUserEnumerationPlugin
from zope.event import notify
import logging


logger = logging.getLogger('PlonePAS')

registerToolInterface('acl_users', IPluggableAuthService)


def _doDelUser(self, id):
    """
    Given a user id, hand off to a deleter plugin if available.
    """
    plugins = self._getOb('plugins')
    import pdb
    pdb.set_trace()
#     context = aq_inner(self)
    mtool = getToolByName(self, 'portal_membership')
    current = mtool.getAuthenticatedMember()
  
    userdeleters = plugins.listPlugins(IUserManagement)

    if not userdeleters:
        raise NotImplementedError(
            "There is no plugin that can delete users."
        )

    for userdeleter_id, userdeleter in userdeleters:
        try:
            user = mtool.getMemberById(id)
            userdeleter.doDeleteUser(id)
        except _SWALLOWABLE_PLUGIN_EXCEPTIONS:
            pass
        else:
            notify(PrincipalDeleted(id))
            notify(DeleteMemberEvent(adminid = current.getId(),
                                     userid = user.getId(),
                                     datetime = '2018-09-09 13:21:22',
                                     ip = '192.168.2.1',
                                     type = 0,
                                     text = "delete user",
                                     result = 1))

wrap_method(
        PluggableAuthService,
        '_doDelUser',
        _doDelUser,
        add=True
    )