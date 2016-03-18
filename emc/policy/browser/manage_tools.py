#-*- coding: UTF-8 -*-
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from Products.Five.browser import BrowserView
from zope.interface import Interface

from zExceptions import NotFound

class Setlayout(BrowserView):
    """
    设置指定内容对象的视图名称，通过:contentobj@@set_layout?new_view_name形式来设置。
    """
    
    implements(IPublishTraverse)      

    
    layout = None
    #receive url parameters
    def publishTraverse(self, request, name):

        if self.layout is None:
            self.layout = name
            return self
        else:
            raise NotFound()
        
    def __call__(self):        
        obj = self.context

        try:
            obj.setLayout(self.layout)
            return "success"
        except:

            return "error"   
    
    