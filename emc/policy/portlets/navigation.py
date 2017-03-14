from plone import api
from Acquisition import aq_inner, aq_base, aq_parent
from ComputedAttribute import ComputedAttribute
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

from plone.app.portlets.portlets.navigation import INavigationPortlet
from plone.app.portlets.portlets.navigation import Assignment as baseAssignment
from plone.app.portlets.portlets.navigation import  Renderer as baseRender
from plone.app.portlets.portlets.navigation import AddForm as baseAddForm
from plone.app.portlets.portlets.navigation import EditForm as baseEditForm
from plone.app.portlets.portlets.navigation import getRootPath

class IEmcNavigationPortlet(INavigationPortlet):
    """
    emc project nav portlet
    """
class ICustomNavigationQueryBuilder(INavigationQueryBuilder): 
    """ custom query builder   
    """
    

class ICustomNavtreeStrategy(INavtreeStrategy):
    """custom strategy for
    """

# @implementer(ICustomNavtreeStrategy)
class CustomNavtreeStrategy(SitemapNavtreeStrategy):
    """Basic navigation tree strategy that does nothing.
    """

    implements(ICustomNavtreeStrategy)
    adapts(Interface, IEmcNavigationPortlet)

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
        if not api.user.has_permission("emc.project:Read project",username=self.memberId,obj=node['item'].getObject()):
            return False
            
        return not getattr(node['item'], 'exclude_from_nav', False)
        
    def decoratorFactory(self,node):
        """Inject any additional keys in the node that are needed and return
        the new node.
        """
        context = aq_inner(self.context)
        request = context.REQUEST

        newNode = node.copy()
        item = node['item']

        portalType = getattr(item, 'portal_type', None)
        itemUrl = item.getURL()
        if portalType is not None and portalType in self.viewActionTypes:
            itemUrl += '/@@ajax_listings'

        useRemoteUrl = False
        getRemoteUrl = getattr(item, 'getRemoteUrl', None)
        isCreator = self.memberId == getattr(item, 'Creator', None)
        if getRemoteUrl and not isCreator:
            useRemoteUrl = True

        isFolderish = getattr(item, 'is_folderish', None)
        showChildren = False
        if isFolderish and \
                (portalType is None or portalType not in self.parentTypesNQ):
            showChildren = True

        layout_view = getMultiAdapter((context, request), name=u'plone_layout')

        newNode['Title'] = utils.pretty_title_or_id(context, item)
        newNode['id'] = item.getId
        newNode['UID'] = item.UID
        newNode['absolute_url'] = itemUrl
        newNode['getURL'] = itemUrl
        newNode['path'] = item.getPath()
        newNode['Creator'] = getattr(item, 'Creator', None)
        newNode['creation_date'] = getattr(item, 'CreationDate', None)
        newNode['portal_type'] = portalType
        newNode['review_state'] = getattr(item, 'review_state', None)
        newNode['Description'] = getattr(item, 'Description', None)
        newNode['show_children'] = showChildren
        newNode['no_display'] = False  # We sort this out with the nodeFilter
        # BBB getRemoteUrl and link_remote are deprecated, remove in Plone 4
        newNode['getRemoteUrl'] = getattr(item, 'getRemoteUrl', None)
        newNode['useRemoteUrl'] = useRemoteUrl
        newNode['link_remote'] = (
            newNode['getRemoteUrl'] and newNode['Creator'] != self.memberId
        )

        idnormalizer = queryUtility(IIDNormalizer)
        newNode['normalized_portal_type'] = idnormalizer.normalize(portalType)
        newNode['normalized_review_state'] = idnormalizer.normalize(
            newNode['review_state']
        )
        newNode['normalized_id'] = idnormalizer.normalize(newNode['id'])

        return newNode                    

    def subtreeFilter(self, node):
        return True


class QueryBuilder(object):
    """Build a navtree query based on the settings in INavigationSchema
    and those set on the portlet.
    """
    implements(ICustomNavigationQueryBuilder)
    adapts(Interface, IEmcNavigationPortlet)

    def __init__(self, context, portlet):
        self.context = context
        self.portlet = portlet

        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')

        # Acquire a custom nav query if available
        customQuery = getattr(context, 'getCustomNavQuery', None)
        if customQuery is not None and utils.safe_callable(customQuery):
            query = customQuery()
        else:
            query = {}

        # Construct the path query
        root = uuidToObject(portlet.root_uid)

        if root is not None:
            rootPath = '/'.join(root.getPhysicalPath())
        else:
            rootPath = getNavigationRoot(context)
        currentPath = '/'.join(context.getPhysicalPath())

        # If we are above the navigation root, a navtree query would return
        # nothing (since we explicitly start from the root always). Hence,
        # use a regular depth-1 query in this case.

        if currentPath != rootPath and not currentPath.startswith(rootPath + '/'):
            query['path'] = {'query': rootPath, 'depth': 1}
        else:
            query['path'] = {'query': rootPath}
#             query['path'] = {'query': currentPath, 'navtree': 1}

        topLevel = portlet.topLevel
        if topLevel and topLevel > 0:
            query['path']['navtree_start'] = topLevel + 1

        # XXX: It'd make sense to use 'depth' for bottomLevel, but it doesn't
        # seem to work with EPI.

        # Only list the applicable types
        query['portal_type'] = utils.typesToList(context)

        # Apply the desired sort
        sortAttribute = navtree_properties.getProperty('sortAttribute', None)
        if sortAttribute is not None:
            query['sort_on'] = sortAttribute
            sortOrder = navtree_properties.getProperty('sortOrder', None)
            if sortOrder is not None:
                query['sort_order'] = sortOrder

        # Filter on workflow states, if enabled
        registry = getUtility(IRegistry)
        navigation_settings = registry.forInterface(
            INavigationSchema,
            prefix="plone"
        )
        if navigation_settings.filter_on_workflow:
            query['review_state'] = navigation_settings.workflow_states_to_show

        self.query = query

    def __call__(self):
        return self.query


def buildFolderTree(context, obj=None, query={},
                    strategy=NavtreeStrategyBase()):
    """Create a tree structure representing a navigation tree. By default,
    it will create a full "sitemap" tree, rooted at the portal, ordered
    by explicit folder order. If the 'query' parameter contains a 'path'
    key, this can be used to override this. To create a navtree rooted
    at the portal root, set query['path'] to:

        {'query' : '/'.join(context.getPhysicalPath()),
         'navtree' : 1}

    to start this 1 level below the portal root, set query['path'] to:

        {'query' : '/'.join(obj.getPhysicalPath()),
         'navtree' : 1,
         'navtree_start' : 1}

    to create a sitemap with depth limit 3, rooted in the portal:

        {'query' : '/'.join(obj.getPhysicalPath()),
         'depth' : 3}

    The parameters:

    - 'context' is the acquisition context, from which tools will be acquired
    - 'obj' is the current object being displayed.
    - 'query' is a catalog query to apply to find nodes in the tree.
    - 'strategy' is an object that can affect how the generation works. It
        should be derived from NavtreeStrategyBase, if given, and contain:

            rootPath -- a string property; the physical path to the root node.

            If not given, it will default to any path set in the query, or the
            portal root. Note that in a navtree query, the root path will
            default to the portal only, possibly adjusted for any navtree_start
            set. If rootPath points to something not returned by the query by
            the query, a dummy node containing only an empty 'children' list
            will be returned.

            showAllParents -- a boolean property; if true and obj is given,
                ensure that all parents of the object, including any that would
                normally be filtered out are included in the tree.

            supplimentQuery -- a dictionary property; provides
                additional query terms which, if not already present
                in the query, are added.  Useful, for example, to
                affect default sorting or default page behavior.

            nodeFilter(node) -- a method returning a boolean; if this returns
                False, the given node will not be inserted in the tree

            subtreeFilter(node) -- a method returning a boolean; if this
                returns False, the given (folderish) node will not be expanded
                (its children will be pruned off)

            decoratorFactory(node) -- a method returning a dict; this can
                inject additional keys in a node being inserted.

            showChildrenOf(object) -- a method returning True if children of
                the given object (normally the root) should be returned

    Returns tree where each node is represented by a dict:

        item            -   A catalog brain of this item
        depth           -   The depth of this item, relative to the startAt
                            level
        currentItem     -   True if this is the current item
        currentParent   -   True if this is a direct parent of the current item
        children        -   A list of children nodes of this node

    Note: Any 'decoratorFactory' specified may modify this list, but
    the 'children' property is guaranteed to be there.

    Note: If the query does not return the root node itself, the root
    element of the tree may contain *only* the 'children' list.

    Note: Folder default-pages are not included in the returned result.
    If the 'obj' passed in is a default-page, its parent folder will be
    used for the purposes of selecting the 'currentItem'.
    """

    portal_url = getToolByName(context, 'portal_url')
    portal_catalog = getToolByName(context, 'portal_catalog')

    rootPath = strategy.rootPath

    request = getattr(context, 'REQUEST', {})

    # Find the object's path. Use parent folder if context is a default-page


    objPath = None
    objPhysicalPath = None
    if obj is not None:
        objPhysicalPath = obj.getPhysicalPath()
        if utils.isDefaultPage(obj, request):
            objPhysicalPath = objPhysicalPath[:-1]
        objPath = '/'.join(objPhysicalPath)

    portalPath = portal_url.getPortalPath()
    portalObject = portal_url.getPortalObject()

    # Calculate rootPath from the path query if not set.

    if 'path' not in query:
        if rootPath is None:
            rootPath = portalPath
        query['path'] = rootPath
    elif rootPath is None:
        pathQuery = query['path']
        if type(pathQuery) == StringType:
            rootPath = pathQuery
        else:
            # Adjust for the fact that in a 'navtree' query, the actual path
            # is the path of the current context
            if pathQuery.get('navtree', False):
                navtreeLevel = pathQuery.get('navtree_start', 1)
                if navtreeLevel > 1:
                    navtreeContextPath = pathQuery['query']
                    navtreeContextPathElements = navtreeContextPath[
                        len(portalPath)+1:].split('/')
                    # Short-circuit if we won't be able to find this path
                    if len(navtreeContextPathElements) < (navtreeLevel - 1):
                        return {'children': []}
                    rootPath = portalPath + '/' + '/'.join(
                        navtreeContextPathElements[:navtreeLevel-1])
                else:
                    rootPath = portalPath
            else:
                rootPath = pathQuery['query']

    rootDepth = len(rootPath.split('/'))

    # Determine if we need to prune the root (but still force the path to)
    # the parent if necessary

    pruneRoot = False
    if strategy is not None:
        rootObject = portalObject.unrestrictedTraverse(rootPath, None)
        if rootObject is not None:
            pruneRoot = not strategy.showChildrenOf(rootObject)

    # Allow the strategy to suppliment the query for keys not already
    # present in the query such as sorting and omitting default pages
    for key, value in strategy.supplimentQuery.iteritems():
        if key not in query:
            query[key] = value

    results = portal_catalog.searchResults(query)

    # We keep track of a dict of item path -> node, so that we can easily
    # find parents and attach children. If a child appears before its
    # parent, we stub the parent node.

    # This is necessary because whilst the sort_on parameter will ensure
    # that the objects in a folder are returned in the right order relative
    # to each other, we don't know the relative order of objects from
    # different folders. So, if /foo comes before /bar, and /foo/a comes
    # before /foo/b, we may get a list like (/bar/x, /foo/a, /foo/b, /foo,
    # /bar,).

    itemPaths = {}

    # Add an (initially empty) node for the root
    itemPaths[rootPath] = {'children': []}

    # If we need to "prune" the parent (but still allow showAllParent to
    # force some children), do so now
    if pruneRoot:
        itemPaths[rootPath]['_pruneSubtree'] = True

    def insertElement(itemPaths, item, forceInsert=False):
        """Insert the given 'item' brain into the tree, which is kept in
        'itemPaths'. If 'forceInsert' is True, ignore node- and subtree-
        filters, otherwise any node- or subtree-filter set will be allowed to
        block the insertion of a node.
        """
        itemPath = item.getPath()

        itemInserted = (itemPaths.get(
            itemPath, {}).get('item', None) is not None)

        # Short-circuit if we already added this item. Don't short-circuit
        # if we're forcing the insert, because we may have inserted but
        # later pruned off the node
        if not forceInsert and itemInserted:
            return

        itemPhysicalPath = itemPath.split('/')
        parentPath = '/'.join(itemPhysicalPath[:-1])
#         import pdb
#         pdb.set_trace()
        parentPruned = (itemPaths.get(
            parentPath, {}).get('_pruneSubtree', False))

        # Short-circuit if we know we're pruning this item's parent

        # XXX: We could do this recursively, in case of parent of the
        # parent was being pruned, but this may not be a great trade-off

        # There is scope for more efficiency improvement here: If we knew we
        # were going to prune the subtree, we would short-circuit here each
        # time. In order to know that, we'd have to make sure we inserted each
        # parent before its children, by sorting the catalog result set
        # (probably manually) to get a breadth-first search.

        if not forceInsert and parentPruned:
            return

        isCurrent = isCurrentParent = False
        if objPath is not None:
            objpath_startswith_itempath = objPath.startswith(itemPath + '/')
            objpath_bigger_than_itempath = \
                len(objPhysicalPath) > len(itemPhysicalPath)
            if objPath == itemPath:
                isCurrent = True
            elif objpath_startswith_itempath and objpath_bigger_than_itempath:
                isCurrentParent = True

        relativeDepth = len(itemPhysicalPath) - rootDepth

        newNode = {'item': item,
                   'depth': relativeDepth,
                   'currentItem': isCurrent,
                   'currentParent': isCurrentParent, }

        insert = True
        if not forceInsert and strategy is not None:
            insert = strategy.nodeFilter(newNode)
        if insert:
            if strategy is not None:
                newNode = strategy.decoratorFactory(newNode)

            # Tell parent about this item, unless an earlier subtree filter
            # told us not to. If we're forcing the insert, ignore the
            # pruning, but avoid inserting the node twice
            if parentPath in itemPaths:
                itemParent = itemPaths[parentPath]
                if forceInsert:
                    nodeAlreadyInserted = False
                    for i in itemParent['children']:
                        if i['item'].getPath() == itemPath:
                            nodeAlreadyInserted = True
                            break
                    if not nodeAlreadyInserted:
                        itemParent['children'].append(newNode)
                elif not itemParent.get('_pruneSubtree', False):
                    itemParent['children'].append(newNode)
            else:
                itemPaths[parentPath] = {'children': [newNode]}

            # Ask the subtree filter (if any), if we should be expanding this
            # node
            if strategy.showAllParents and isCurrentParent:
                # If we will be expanding this later, we can't prune off
                # children now
                expand = True
            else:
                expand = getattr(item, 'is_folderish', True)
            if expand and (not forceInsert and strategy is not None):
                expand = strategy.subtreeFilter(newNode)

            children = newNode.setdefault('children', [])
            if expand:
                # If we had some orphaned children for this node, attach
                # them
                if itemPath in itemPaths:
                    children.extend(itemPaths[itemPath]['children'])
            else:
                newNode['_pruneSubtree'] = True

            itemPaths[itemPath] = newNode

    # Add the results of running the query
    for r2 in results:

        insertElement(itemPaths, r2)

    # If needed, inject additional nodes for the direct parents of the
    # context. Note that we use an unrestricted query: things we don't normally
    # have permission to see will be included in the tree.
    if strategy.showAllParents and objPath is not None:
        objSubPathElements = objPath[len(rootPath)+1:].split('/')
        parentPaths = []

        haveNode = (itemPaths.get(rootPath, {}).get('item', None) is None)
        if not haveNode:
            parentPaths.append(rootPath)

        parentPath = rootPath
        for i in range(len(objSubPathElements)):
            nodePath = rootPath + '/' + '/'.join(objSubPathElements[:i+1])
            node = itemPaths.get(nodePath, None)

            # If we don't have this node, we'll have to get it, if we have it
            # but it wasn't connected, re-connect it
            if node is None or 'item' not in node:
                parentPaths.append(nodePath)
            else:
                nodeParent = itemPaths.get(parentPath, None)
                if nodeParent is not None:
                    nodeAlreadyInserted = False
                    for i in nodeParent['children']:
                        if i['item'].getPath() == nodePath:
                            nodeAlreadyInserted = True
                            break
                    if not nodeAlreadyInserted:
                        nodeParent['children'].append(node)

            parentPath = nodePath

        # If we were outright missing some nodes, find them again
        if len(parentPaths) > 0:
            query = {'path': {'query': parentPaths, 'depth': 0}}
            results = portal_catalog.unrestrictedSearchResults(query)

            for r in results:
                insertElement(itemPaths, r, forceInsert=True)

    # Return the tree starting at rootPath as the root node.

    return itemPaths[rootPath]   


class Assignment(baseAssignment):
    """emc nav portlet assignment
    """
    implements(IEmcNavigationPortlet)

class Renderer(baseRender):
    
    def createNavTree(self):
        data = self.getNavTree()
        bottomLevel = self.data.bottomLevel or 0
        
        if bottomLevel < 0:
            # Special case where navigation tree depth is negative
            # meaning that the admin does not want the listing to be displayed
            return self.recurse([], level=1, bottomLevel=bottomLevel)
        else:
            return self.recurse(children=data.get('children', []), level=1, bottomLevel=bottomLevel)
    
    _template = ViewPageTemplateFile('navigation.pt')
    recurse = ViewPageTemplateFile('emc_navigation_recurse.pt')

    @memoize
    def getNavTree(self, _marker=None):
        if _marker is None:
            _marker = []
        context = aq_inner(self.context)
#         import pdb
#         pdb.set_trace()
        queryBuilder = getMultiAdapter((context, self.data), INavigationQueryBuilder)
        strategy = getMultiAdapter((context, self.data), ICustomNavtreeStrategy)
        return buildFolderTree(context, obj=context, query=queryBuilder(), strategy=strategy)


class AddForm(baseAddForm):
    schema = IEmcNavigationPortlet
    def create(self, data):
        return Assignment(name=data.get('name', ""),
                          root_uid=data.get('root_uid', ""),
                          currentFolderOnly=data.get('currentFolderOnly', False),
                          includeTop=data.get('includeTop', False),
                          topLevel=data.get('topLevel', 0),
                          bottomLevel=data.get('bottomLevel', 0))

class EditForm(baseEditForm):
    schema = INavigationPortlet