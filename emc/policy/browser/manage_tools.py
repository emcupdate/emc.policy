#-*- coding: UTF-8 -*-
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from Products.Five.browser import BrowserView
from zope.interface import Interface

from zExceptions import NotFound

class Setlayout(BrowserView):
    
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
    
    