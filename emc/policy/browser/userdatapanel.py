# -*- coding: utf-8 -*-
from plone.app.users.browser.userdatapanel import UserDataPanel
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class UserDataConfiglet(UserDataPanel):
    """Control panel version of the userdata panel"""
    template = ViewPageTemplateFile('templates/account-configlet.pt')
