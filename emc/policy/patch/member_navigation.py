from plone import api
from Acquisition import aq_inner, aq_base, aq_parent
from ComputedAttribute import ComputedAttribute
from types import StringType
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.navigation.interfaces import INavtreeStrategy
# from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.navtree import NavtreeStrategyBase
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.portlets import base
from plone.app.uuid.utils import uuidToObject
from plone.app.vocabularies.catalog import CatalogSource
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.registry.interfaces import IRegistry
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.interfaces import IBrowserDefault
from Products.CMFPlone import utils
from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy
from Products.CMFPlone.defaultpage import is_default_page
from Products.CMFPlone.interfaces import INavigationSchema
from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zExceptions import NotFound
from zope import schema
from zope.component import adapts, getMultiAdapter, queryUtility
from zope.component import getUtility
from zope.interface import implements, Interface
from zope.interface import implementer
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.portlets.portlets.navigation import INavigationPortlet
from plone.app.portlets.portlets.navigation import Assignment as baseAssignment
from plone.app.portlets.portlets.navigation import  Renderer as baseRender
from plone.app.portlets.portlets.navigation import AddForm as baseAddForm
from plone.app.portlets.portlets.navigation import EditForm as baseEditForm
from plone.app.portlets.portlets.navigation import getRootPath




class IMembersNavtreeStrategy(INavtreeStrategy):
    """custom strategy for member path
    """


class MembersNavtreeStrategy(SitemapNavtreeStrategy):
    """navigation tree strategy for project management.
    """

    implements(IMembersNavtreeStrategy)
    adapts(Interface, INavigationPortlet)

    def __init__(self, context, portlet):
        SitemapNavtreeStrategy.__init__(self, context, portlet)

        # XXX: We can't do this with a 'depth' query to EPI...
        membership = getToolByName(context, 'portal_membership')
        self.memberId = membership.getAuthenticatedMember().getId()
        self.bottomLevel = portlet.bottomLevel or 0

        self.rootPath = getRootPath(context,
                                    portlet.currentFolderOnly,
                                    portlet.topLevel,
                                    portlet.root_uid)    

    # Default sorting and allow display default-pages
#     supplimentQuery = {'sort_on': 'getObjPositionInParent'}    
    
    
    def nodeFilter(self,node):
        """Return True or False to determine whether to include the given node
        in the tree. Nodes are dicts with at least one key - 'item', the
        catalog brain of the object the node represents.
        """
        path = node['item'].getPath()
        obj = node['item'].getObject()
        if path.find("Members") >=0:
#             api.user.get_roles(username='jane', obj=portal['blog'])
            if "Owner" not in api.user.get_roles(username=self.memberId,obj=obj):
                return False
            
        return not getattr(node['item'], 'exclude_from_nav', False)
        
#     def decoratorFactory(self,node):
#         """Inject any additional keys in the node that are needed and return
#         the new node.
#         """
#         context = aq_inner(self.context)
#         request = context.REQUEST
# 
#         newNode = node.copy()
#         item = node['item']
# 
#         portalType = getattr(item, 'portal_type', None)
#         itemUrl = item.getURL()
#         if portalType is not None and portalType in self.viewActionTypes:
#             itemUrl += '/@@ajax_listings'
# 
#         useRemoteUrl = False
#         getRemoteUrl = getattr(item, 'getRemoteUrl', None)
#         isCreator = self.memberId == getattr(item, 'Creator', None)
#         if getRemoteUrl and not isCreator:
#             useRemoteUrl = True
# 
#         isFolderish = getattr(item, 'is_folderish', None)
#         showChildren = False
#         if isFolderish and \
#                 (portalType is None or portalType not in self.parentTypesNQ):
#             showChildren = True
# 
#         layout_view = getMultiAdapter((context, request), name=u'plone_layout')
# 
#         newNode['Title'] = utils.pretty_title_or_id(context, item)
#         newNode['id'] = item.getId
#         newNode['UID'] = item.UID
#         newNode['absolute_url'] = itemUrl
#         newNode['getURL'] = itemUrl
#         newNode['path'] = item.getPath()
#         newNode['Creator'] = getattr(item, 'Creator', None)
#         newNode['creation_date'] = getattr(item, 'CreationDate', None)
#         newNode['portal_type'] = portalType
#         newNode['review_state'] = getattr(item, 'review_state', None)
#         newNode['Description'] = getattr(item, 'Description', None)
#         newNode['show_children'] = showChildren
#         newNode['no_display'] = False  # We sort this out with the nodeFilter
#         # BBB getRemoteUrl and link_remote are deprecated, remove in Plone 4
#         newNode['getRemoteUrl'] = getattr(item, 'getRemoteUrl', None)
#         newNode['useRemoteUrl'] = useRemoteUrl
#         newNode['link_remote'] = (
#             newNode['getRemoteUrl'] and newNode['Creator'] != self.memberId
#         )
# 
#         idnormalizer = queryUtility(IIDNormalizer)
#         newNode['normalized_portal_type'] = idnormalizer.normalize(portalType)
#         newNode['normalized_review_state'] = idnormalizer.normalize(
#             newNode['review_state']
#         )
#         newNode['normalized_id'] = idnormalizer.normalize(newNode['id'])
# 
#         return newNode                    
# 
#     def subtreeFilter(self, node):
#         return True





def getNavTree(self, _marker=None):
        if _marker is None:
            _marker = []
        context = aq_inner(self.context)
#         import pdb
#         pdb.set_trace()
        queryBuilder = getMultiAdapter((context, self.data), INavigationQueryBuilder)
        strategy = getMultiAdapter((context, self.data), IMembersNavtreeStrategy)
        return buildFolderTree(context, obj=context, query=queryBuilder(), strategy=strategy)


