# -*- coding: utf-8 -*-
from plone.app.contenttypes.browser.utils import Utils
from AccessControl import getSecurityManager
# from AccessControl import Unauthorized
from Products.CMFCore.permissions import ModifyPortalContent

class FileView(Utils):

    def __init__(self, context, request):
        super(FileView, self).__init__(context, request)

    def is_videotype(self):
        ct = self.context.file.contentType
        return 'video/' in ct

    def is_audiotype(self):
        ct = self.context.file.contentType
        return 'audio/' in ct

    def get_mimetype_icon(self):
        return super(FileView, self).getMimeTypeIcon(self.context.file)
    
    def isEditable(self):
        sm = getSecurityManager()
        return sm.checkPermission(ModifyPortalContent, self.context)
    
    def txtgoodcode(self):
        
        data = self.context.file.data
        sourceFormats = ['cp936','utf-8']
        for format in sourceFormats:
            try:
#                 import pdb
#                 pdb.set_trace()
                return data.decode(format).encode('utf-8')
            except:
                pass
                
            
