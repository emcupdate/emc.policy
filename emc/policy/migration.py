# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from zope.container.interfaces import INameChooser
from zope.component import getUtility
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from emc.project.content.projectfolder import IProjectFolder
from emc.policy.portlets import navigation



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
    assignment = navigation.Assignment(name=u"项目导航",root_uid=obj.UID(),topLevel=0)
    chooser = INameChooser(manager)
    manager[chooser.chooseName(None, assignment)] = assignment 
    


