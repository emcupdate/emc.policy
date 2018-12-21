# -*- coding: utf-8 -*-
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import provider
from Products.CMFPlone import PloneMessageFactory as _
"""
非密  60
内部  65
一般  70
重要  80
核心  90
空值 100
"""

# items = [ ('low', _('secret')),
#           ('mid', _('more secret')),
#           ('height', _('most secret'))          
#           ]
items = [ ('60', _('no secret')),
          ('65', _('inner')),
          ('70', _('normal secret')), 
          ('80', _('more secret')),
          ('90', _('most secret')),
          ('100', _('Null')),                     
          ]
terms = [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items ]
Vocabulary = SimpleVocabulary(terms)

@provider(IVocabularyFactory)
def safe_level_factory(context):
    return Vocabulary