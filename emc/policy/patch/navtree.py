# -*- coding: utf-8 -*-
# This module contains a function to help build navigation-tree-like structures
# from catalog queries. It also contains a standard implementation of the
# strategy/filtering method that uses Plone's navtree_properties to construct
# navtrees.
from AccessControl import ModuleSecurityInfo
from Acquisition import aq_inner
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import NavtreeStrategyBase
from plone.app.layout.navigation.root import getNavigationRoot
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from Products.CMFPlone.interfaces import INavigationSchema
from zope.component import getMultiAdapter, queryUtility
from zope.component import getUtility
from zope.interface import implementer


def showChildrenOf(self, object):
    getTypeInfo = getattr(object, 'getTypeInfo', None)
    if getTypeInfo is not None:
        try:
            portal_type = getTypeInfo().getId()
        except:
            return True                
        if portal_type in self.parentTypesNQ:
            return False
