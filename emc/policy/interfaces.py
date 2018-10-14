#-*- coding: UTF-8 -*-
from zope import schema
from zope.interface import Interface
from zope.interface import Attribute
from emc.policy import MessageFactory as _
# event
   
class IAddloginEvent(Interface):
    """用户登陆事件"""


class IAddlogoutEvent(Interface):
    """用户注销事件"""
    
          
class IDeleteMemberEvent(Interface):
    """ manager through user&group controlpanel delete the specify member,fire this event"""
    adminid = Attribute("system administrator's id")
    userid = Attribute("id of user that will be deleted by system administrator ")
    datetime = Attribute("the datetime of executing delete action.format:'2018-09-09 20:12:24'")
    ip = Attribute("ip address of the system administrator login in ")
    type =  Attribute("the operation's type")
    description =   Attribute("the operation's content")
    result = Attribute("the operation's result")

class ICreateMemberEvent(Interface):
    """ manager through user&group controlpanel create the specify member,fire this event"""
    adminid = Attribute("system administrator's id")
    userid = Attribute("id of user that will be created by system administrator ")
    datetime = Attribute("the datetime of executing create action.format:'2018-09-09 20:12:24'")
    ip = Attribute("ip address of the system administrator login in ")
    type =  Attribute("the operation's type")
    description =   Attribute("the operation's content")
    result = Attribute("the operation's result")
 
class IChangeMemberEvent(Interface):
    """ manager through user&group controlpanel change the specify member,fire this event"""
    adminid = Attribute("system administrator's id")
    userid = Attribute("id of user that will be changed by system administrator ")
    datetime = Attribute("the datetime of executing change action.format:'2018-09-09 20:12:24'")
    ip = Attribute("ip address of the system administrator login in ")
    type =  Attribute("the operation's type")
    description =   Attribute("the operation's content")
    result = Attribute("the operation's result")
        
# Database event
class ILocalize_time(Interface):
    def localize(self,time):
        """
        """

class IRolesLocator(Interface):
    def GetAllRole(self):
        """获取所有的角色,返回list"""
    
class IUserroleLocator(Interface):
    def GetRoleAllUser(self,role):
        """获取指定角色中所有用户信息,返回对象list"""
        
    def GetUserAllRole(self,user):
        """获取指定用户所有角色信息,返回对象list"""
        
class IAdminlogsLocator(Interface):
    def Getconditionsadminlogs(self,conditions="1"):
        """根据指定sql条件查询系统日志,"""
    
class ILoginlogsLocator(Interface):
    def Getconditionsloginlogs(self,conditions="1"):
        """根据指定sql条件查询登录日志,"""
class IContracthistoryLocator(Interface): 
    def GetContracthistory(self,channelid):
        """根据渠道channelid获取所有到签约历史记录"""
######
class ILocalRoleProvider(Interface):
    """注册管理角色"""
    def getRole(principal_id):
        """Returns an iterable of roles granted to specified user object
        """
    def getAllRoles(self):
        """Returns an iterable consisting of tuples of the form:
        """
        
