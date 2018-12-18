#-*- coding: UTF-8 -*-
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent
from emc.policy.utils import CheckLog
from emc.policy.utils import send_warning
from plone import api


def UserLogoutEventHandler(event):
    """normal users logout event handler"""
    
    from emc.kb.interfaces import IUserLogLocator
#     dbapi,timeout,bsize,percentage,max = fetch_log_parameter('userlog')  
#     # check log size and send warning
#     userid = '444444555555666666'
#     url = "%s/@@user_logs" % api.portal.get().absolute_url()      
#     check_size(dbapi,percentage,max,userid,url)      
#     # truncate log      
#     task = CheckLog(3,dbapi,timeout,bsize,max,percentage)
#     task.start()
    
    values = {'userid':event.userid,'datetime':event.datetime,
              'ip':event.ip,'type':0,'operlevel':4,'result':1,'description':u''}                
    values['description'] = u"%s登出了EMC系统" % (event.userid)  
    locator = getUtility(IUserLogLocator)
    locator.add(values)

def fetch_log_parameter(table):
    "fetch log system's settings"
    from emc.kb.interfaces import IDbapi
    from zope.component import queryUtility    
#     from emc.policy.utils import CheckLog
    from plone.registry.interfaces import IRegistry
    from emc.kb.interfaces import ILogSettings
    dbapi = queryUtility(IDbapi, name=table)
    registry = getUtility(IRegistry)        
    settings = registry.forInterface(ILogSettings, check=False)
    timeout = settings.timeout
    bsize = settings.bsize
    percentage = settings.percentage
    max = settings.max
    return (dbapi,timeout,bsize,percentage,max)    

def check_size(dbapi,percentage,max,userid,url):
    "check table size and send warning message"
    
    # check log size
    recorders = dbapi.get_rownumber()
    tmp = int(max * percentage)
    if recorders >= tmp and recorders <= tmp + 1:
#         userid = 'test17'
#         url = ''
        send_warning(percentage,userid,url)        
    
def UserLoginEventHandler(event):
    """normal users login event handler"""
    
    from emc.kb.interfaces import IUserLogLocator
#     dbapi,timeout,bsize,percentage,max = fetch_log_parameter('userlog')  
#     # check log size and send warning
#     userid = '444444555555666666'
#     url = "%s/@@user_logs" % api.portal.get().absolute_url()      
#     check_size(dbapi,percentage,max,userid,url)      
#     # truncate log      
#     task = CheckLog(3,dbapi,timeout,bsize,max,percentage)
#     task.start()
    
    values = {'userid':event.userid,'datetime':event.datetime,
              'ip':event.ip,'type':0,'operlevel':4,'result':1,'description':u''}                
    if event.description == "":
        values['description'] = u"%s登入了EMC系统" % (event.userid)
    else:
        values['description'] = u"%s%s" % (event.userid,event.description)  
    locator = getUtility(IUserLogLocator)
    locator.add(values)

def AdminLogoutEventHandler(event):
    """the system administrators logout event handler"""

    from emc.kb.interfaces import IAdminLogLocator
    dbapi,timeout,bsize,percentage,max = fetch_log_parameter('adminlog')  
    # check log size and send warning
    userid = '777777888888999999'
    url = "%s/@@admin_logs" % api.portal.get().absolute_url()      
    check_size(dbapi,percentage,max,userid,url)      
    # truncate log      
    task = CheckLog(8,dbapi,timeout,bsize,max,percentage)
    task.start()
    
    values = {'adminid':event.adminid,'userid':' ','datetime':event.datetime,
              'ip':event.ip,'type':0,'operlevel':4,'result':1,'description':u''}                
    if event.description == "":
        values['description'] = u"%s登出了EMC系统" % (event.adminid)
    else:
        values['description'] = u"%s%s" % (event.adminid,event.description)          
    locator = getUtility(IAdminLogLocator)
    locator.add(values)

def AdminLoginEventHandler(event):
    """the system administrators login event handler"""
    from emc.kb.interfaces import IAdminLogLocator
    dbapi,timeout,bsize,percentage,max = fetch_log_parameter('adminlog')  
    # check log size and send warning
    userid = '777777888888999999'
    url = "%s/@@admin_logs" % api.portal.get().absolute_url()      
    check_size(dbapi,percentage,max,userid,url)      
    # truncate log      
    task = CheckLog(8,dbapi,timeout,bsize,max,percentage)
    task.start()
    
    values = {'adminid':event.adminid,'userid':' ','datetime':event.datetime,
              'ip':event.ip,'type':0,'operlevel':4,'result':1,'description':u''}                
    values['description'] = u"%s登陆了EMC系统" % (event.adminid)  
    locator = getUtility(IAdminLogLocator)
    locator.add(values)
    
def DeleteMemberEventHandler(event):
    """the system administrator delete specify user handler"""
    from emc.kb.interfaces import IAdminLogLocator,IDbapi
    from zope.component import getUtility,queryUtility
    dbapi = queryUtility(IDbapi, name="adminlog")
#     rt = check_log(dbapi)
    
    values = {'adminid':event.adminid,'userid':event.userid,'datetime':event.datetime,
              'ip':event.ip,'type':0,'operlevel':4,'result':1,'description':u''}                
    values['description'] = u"管理员%s删除了%s" % (event.adminid,event.userid)  
    locator = getUtility(IAdminLogLocator)
    locator.add(values)
    
def CreateMemberEventHandler(event):
    """the system administrator create specify user handler"""
    from emc.kb.interfaces import IAdminLogLocator,IDbapi
    from zope.component import getUtility,queryUtility
    dbapi = queryUtility(IDbapi, name="adminlog")
#     rt = check_log(dbapi)
    
    values = {'adminid':event.adminid,'userid':event.userid,'datetime':event.datetime,
              'ip':event.ip,'type':0,'operlevel':4,'result':1,'description':u''}                
    values['description'] = u"管理员%s创建了%s%s" % (event.adminid,event.userid,event.description)  
    locator = getUtility(IAdminLogLocator)
    locator.add(values)
    
def ChangeMemberEventHandler(event):
    """the system administrator change specify user handler"""
    from emc.kb.interfaces import IAdminLogLocator,IDbapi
    from zope.component import getUtility,queryUtility
    dbapi = queryUtility(IDbapi, name="adminlog")
#     rt = check_log(dbapi)
    
    values = {'adminid':event.adminid,'userid':event.userid,'datetime':event.datetime,
              'ip':event.ip,'type':0,'operlevel':4,'result':1,'description':u''}                
    values['description'] = u"管理员%s修改了%s:%s" % (event.adminid,event.userid,event.description)  

    locator = getUtility(IAdminLogLocator)
    locator.add(values)
         
  

def userLoginedIn(event):
    """Redirects  logged in users to getting started wizard"""  

    portal = getSite() 
    user = event.object
    # admin by pass
    if user.getUserName() == "admin":return
    # check if we have an access to request object
    request = getattr(portal, 'REQUEST', None)
    if not request:
        return  
    # now complile and render our expression to url

    try:
        member_url_view = getMultiAdapter((portal, request),name=u"member_url") 
        url = member_url_view()
    except Exception, e:
        logException(u'Error during user login in redirect')
        return
    else:
        # check if came_from is not empty, then clear it up, otherwise further
        # Plone scripts will override our redirect
        if request.get('came_from'):
            request['came_from'] = ''
            request.form['came_from'] = ''
        request.RESPONSE.redirect(url) 