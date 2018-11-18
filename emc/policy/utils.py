from zope.component import getUtility
from Products.CMFCore.interfaces import IPropertiesTool
from plone.registry.interfaces import IRegistry


def getDropdownDepth():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('dropdown_depth')


def cachingEnabled():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('enable_caching', False)


def parentClickable():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('enable_parent_clickable', True)

def check_log(dbapi):
    "check log db,iff touch to max recorders and iff touch to the longest reserved time"
    
    from emc.kb.interfaces import ILogSettings
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
    
    
