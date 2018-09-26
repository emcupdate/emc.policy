#-*- coding: UTF-8 -*-
from zope import interface
from zope.component import adapts
from zope.component.interfaces import ObjectEvent

from emc.policy.interfaces import IAddloginlogsEvent,IAddlogoutlogsEvent,INormaladminlogsEvent
from emc.policy.interfaces import ICreateMemberEvent
from emc.policy.interfaces import IChangeMemberEvent
from emc.policy.interfaces import IDeleteMemberEvent

# class logsEvent

class AddloginlogsEvent(ObjectEvent):
    interface.implements(IAddloginlogsEvent)


class AddlogoutlogsEvent(ObjectEvent):
    interface.implements(IAddlogoutlogsEvent)
    
    
class NormaladminlogsEvent(object):
    interface.implements(INormaladminlogsEvent)
    
    def __init__(self,rolename,levelname,elevelname,description):
        """角色,级别,备注"""
        self.rolename = rolename
        self.levelname = levelname
        self.elevelname = elevelname
        self.description = description
     
class DeleteMemberEvent(object):
    """manager through user&group controlpanel delete the specify member,fire this event"""
    interface.implements(IDeleteMemberEvent)
    
    def __init__(self,adminid,userid,datetime,ip,type,description,result):
        self.adminid = adminid
        self.userid = userid
        self.datetime = datetime
        self.ip = ip
        self.type = type
        self.description = description
        self.result = result         


class CreateMemberEvent(object):
    """manager through user&group controlpanel create the specify member,fire this event"""
    interface.implements(ICreateMemberEvent)
    def __init__(self,adminid,userid,datetime,ip,type,description,result):
        self.adminid = adminid
        self.userid = userid
        self.datetime = datetime
        self.ip = ip
        self.type = type
        self.description = description
        self.result = result   


class ChangeMemberEvent(object):
    """manager through user&group controlpanel change the specify member,fire this event"""
    interface.implements(IChangeMemberEvent)
    def __init__(self,adminid,userid,datetime,ip,type,description,result):
        self.adminid = adminid
        self.userid = userid
        self.datetime = datetime
        self.ip = ip
        self.type = type
        self.description = description
        self.result = result 