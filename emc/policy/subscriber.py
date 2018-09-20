#-*- coding: UTF-8 -*-
from zope.component import getMultiAdapter
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent

def DeleteMemberEventHandler(event):
    """the system administrator delete specify user handler"""
    import pdb
    pdb.set_trace()    
    print event.adminid
    
def PrincipalDeletedHandler(event):
    """the pluggableAuthService delete member event's handler"""
    
    import pdb
    pdb.set_trace()
    print event.principal
    

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