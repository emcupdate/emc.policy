#-*- coding: UTF-8 -*-
# from __future__ import division
from zope.component import getUtility
from zope.event import notify
from Products.CMFCore.interfaces import IPropertiesTool
from emc.memberArea.events import TodoitemWillCreateEvent
import logging
import datetime
import threading
import time

def getDropdownDepth():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('dropdown_depth')


def cachingEnabled():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('enable_caching', False)


def parentClickable():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('enable_parent_clickable', True)

def send_warning(percentage,userid,url):
        "send warning to administrators"

        title = "警告:系统日志已达到%.0f%%临界点!" % (percentage *100)
        text = u"""<p>请通过<a href="%s"><strong>日志管理页面</strong></a>提前备份日志</p>""" %(url)
        notify(TodoitemWillCreateEvent(title=title,userid=userid,sender="System",text=text))       

def check_log(dbapi):
    "check log db,iff touch to max recorders and iff touch to the longest reserved time"
    
    from emc.kb.interfaces import ILogSettings
    from plone.registry.interfaces import IRegistry
    import datetime
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ILogSettings, check=False)
    timeout = settings.timeout
    bsize = settings.bsize
    max = settings.max
    recorders = dbapi.get_rownumber()
    if recorders <= max:return 0
    old = dbapi.fetch_oldest()
    differ = (datetime.datetime.now() -old).days()
    if differ > timeout:
        dbapi.bulk_delete(bsize)
        return 1
    else:
        return 0
    
class CheckLog (threading.Thread):
    def __init__(self, time, dbapi,timeout,bsize,max,percentage):
      threading.Thread.__init__(self)
      self._stop_event = threading.Event()
      self.time = time
      self.dbapi = dbapi
      self.timeout = timeout
      self.bsize = bsize
      self.max = max
      self.percentage = percentage      
    
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
    def run(self):
       
        nw = time.localtime().tm_hour
        if nw >= self.time and self.recorders > self.max:
            self.check_log(self.dbapi,self.timeout,self.bsize,self.max)
            return
        else:
            return
         
           
    def check_log(self,dbapi,timeout,bsize,max):
        "check log db,iff touch to max recorders and iff touch to the longest reserved time"    

        recorders = dbapi.get_rownumber()
        logging.info("im am in check_log")
# 
        if recorders <= max:return 0
        old = dbapi.fetch_oldest()
        differ = (datetime.datetime.now() -old).days()
        if differ > timeout:
            dbapi.bulk_delete(bsize)
            return 1
        else:
            return 0
        
    def send_warning(self,percentage):
        "send warning to administrators"
        title = "警告:系统日志已达到%s临界点!" % percentage
        userid = 'test17'
        url = ''
        text = u"""<p>请通过<a href="%s"><strong>日志管理页面</strong></a>提前备份日志</p>""" %(url)
        notify(TodoitemWillCreateEvent(title=title,userid=userid,sender="System",text=text))       

        
