#-*- coding: UTF-8 -*-
from zope import interface
from zope.component import adapts
from zope.component.interfaces import ObjectEvent
from plone import api
from emc.policy.interfaces import IAddloginEvent,IAddlogoutEvent
from emc.policy.interfaces import ICreateMemberEvent
from emc.policy.interfaces import IChangeMemberEvent
from emc.policy.interfaces import IDeleteMemberEvent

# class logsEvent
class EventFilter(object):
    """
    if current user has 'manager' role,cancel log event
    """
    def __init__(self,adminid,userid,datetime,ip,type,description,result):
        self.adminid = adminid
        self.userid = userid
        self.datetime = datetime
        self.ip = ip
        self.type = type
        self.description = description
        self.result = result
    
    def available(self):
        try:
            roles = api.user.get_roles()
            return not('Manager' in roles)
        except:
            return True

class AddloginEvent(EventFilter):
    interface.implements(IAddloginEvent)
      

class AddlogoutEvent(EventFilter):
    interface.implements(IAddlogoutEvent)
           
     
class DeleteMemberEvent(EventFilter):
    """manager through user&group controlpanel delete the specify member,fire this event"""
    interface.implements(IDeleteMemberEvent)           


class CreateMemberEvent(EventFilter):
    """manager through user&group controlpanel create the specify member,fire this event"""
    interface.implements(ICreateMemberEvent)


class ChangeMemberEvent(EventFilter):
    """manager through user&group controlpanel change the specify member,fire this event"""
    interface.implements(IChangeMemberEvent)
