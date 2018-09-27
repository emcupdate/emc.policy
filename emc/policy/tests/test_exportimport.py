# -*- coding: utf-8 -*-
from plone.app.testing.bbb import PloneTestCase
from plone.app.users.browser.userdatapanel import getUserDataSchema
from plone.app.users.setuphandlers import export_schema
from plone.app.users.setuphandlers import import_schema
from plone.app.users.testing import PLONE_APP_USERS_FUNCTIONAL_TESTING
from plone.namedfile.field import NamedBlobImage
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.tests.common import DummyExportContext
from Products.GenericSetup.tests.common import DummyImportContext
from zope import schema


class TestImport(PloneTestCase):

    layer = PLONE_APP_USERS_FUNCTIONAL_TESTING

    def afterSetUp(self):
        xml = """<model xmlns:lingua="http://namespaces.plone.org/supermodel/lingua" xmlns:users="http://namespaces.plone.org/supermodel/users" xmlns:form="http://namespaces.plone.org/supermodel/form" xmlns:i18n="http://xml.zope.org/namespaces/i18n" xmlns:security="http://namespaces.plone.org/supermodel/security" xmlns:marshal="http://namespaces.plone.org/supermodel/marshal" xmlns="http://namespaces.plone.org/supermodel/schema" i18n:domain="plone">
    <schema name="member-fields">
    <field name="id_number" type="zope.schema.TextLine"
      users:forms="In User Profile">
      <description i18n:translate="help_idnumber">
          The number of user's personal identifier .
      </description>
      <required>True</required>
      <title i18n:translate="">Identifier Number</title>
    </field>
    <field name="safe_level" type="zope.schema.Choice" users:forms="In User Profile">
      <description/>
      <required>False</required>
      <title i18n:translate="">safe level</title>
      <values>
        <element>height</element>
        <element>mid</element>
        <element>low</element>
      </values>
    </field>
  </schema>
</model>
"""
        context = DummyImportContext(self.portal, purge=False)
        context._files = {'userschema.xml': xml}
        import_schema(context)

    def test_import(self):
        user_schema = getUserDataSchema()
        pm = getToolByName(self.portal, "portal_memberdata")
        member_properties = pm.propertyIds()

        self.assertIn("id_number", user_schema)
        self.assertTrue(isinstance(user_schema['id_number'], schema.TextLine))
        self.assertIn("id_number", member_properties)
        self.assertEqual(pm.getPropertyType('id_number'), 'string')

        self.assertIn("safe_level", user_schema)
        self.assertTrue(isinstance(user_schema['safe_level'], schema.Choice))
        self.assertIn("safe_level", member_properties)
        self.assertEqual(pm.getPropertyType('safe_level'), 'string')

    def test_export(self):
        context = DummyExportContext(self.portal)
        export_schema(context)
        self.assertEqual('userschema.xml', context._wrote[0][0])
        self.assertIn('field name="id_number"', context._wrote[0][1])
        self.assertIn('field name="safe_level"', context._wrote[0][1])        

