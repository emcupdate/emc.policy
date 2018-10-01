# -*- coding: utf-8 -*-
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFCore.utils import getToolByName
from zope.container.interfaces import INameChooser
from zope.component import getUtility
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from emc.project.content.projectfolder import IProjectFolder
from emc.policy.portlets import navigation

def setupGroups(context):

#     import pdb
#     pdb.set_trace()
    group = api.group.create(
            groupname='System Administrators',
            title='System Administrators',
            description='EMC System Administrators',
            roles=['SysAdmin','Site Administrator', ],
            ) 
    group = api.group.create(
            groupname='Secure Staffs',
            title='Secure Staffs',
            description='EMC Secure Staffs',
            roles=['SecStaff','Site Administrator', ],
            ) 
    group = api.group.create(
            groupname='Secure Auditors',
            title='Secure Auditors',
            description='EMC Secure Auditors',
            roles=['SecAuditor','Site Administrator', ],
            )
#     for i in range(1,3):            
#         api.user.create(
#             username='master%s' % i,
#             email='master%s@plone.org' % i,
#             password='secret$',
#                                ) 
    api.group.add_user(groupname='System Administrators', username='test17')
    api.group.add_user(groupname='Secure Staffs', username='test18')
    api.group.add_user(groupname='Secure Auditors', username='test19')

def add_navigator_portlet(context):
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":IProjectFolder.__identifier__}
    bns = pc(query)
    if len(bns) == 0: return
    obj = bns[0].getObject()
    column = getUtility(IPortletManager, name=u"plone.leftcolumn")
    
    # We multi-adapt the object and the column to an assignment mapping,
    # which acts like a dict where we can put portlet assignments
    manager = getMultiAdapter((obj, column,), IPortletAssignmentMapping)
    
    # We then create the assignment and put it in the assignment manager,
    # using the default name-chooser to pick a suitable name for us.
    assignment = navigation.Assignment(name=u"项目管理",root_uid=obj.UID(),topLevel=0)
    chooser = INameChooser(manager)
    manager[chooser.chooseName(None, assignment)] = assignment

#     loadMigrationProfile(context, 'profile-emc.policy:to507')
 
    


