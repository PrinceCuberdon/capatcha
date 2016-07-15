# -*- coding: UTF-8 -*-
# capatcha is part of Band Cochon
# Band Cochon (c) Prince Cuberdon 2011 and Later <princecuberdon@bandcochon.fr>


import os

from django.test import TestCase
from django.template import RequestContext, Template
from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.base import SessionBase
from django.conf import settings

from .models import Preference
from .templatetags.capatcha_tags import Capatcha


class TestCapatcha(TestCase):
    def setUp(self):
        """ Create a dummy capatcha 
        FIXME: Move to MEDIA_URL + CAPATCHA_CONFIG.Download image and font from tests/resources/
        """
        self.cap = Preference.objects.create(
            font="capatcha/ACIDIC.ttf",
            background="capatcha/antispam.png"
        )

    def test_tag(self):
        """ Test the template tag. 
        Our user have no sessionkey so the sessionkey is None, the image is called None.png 
        """

        tpl = u'''{% load capatcha_tags %}{% create_capatcha %}{{ capatcha.path }}'''
        # Simulate a request
        req = HttpRequest()
        req.user = AnonymousUser()
        req.session = SessionBase()
        result = Template(tpl).render(RequestContext(req))
        # Replace because of Windows Platform
        self.assertEqual(result, os.path.join(settings.MEDIA_URL, settings.CAPATCHA_CONFIG.temp, u"None.png").replace('\\', '/'))

    def test_capatcha_object_remove_old(self):
        """ this can't be tested here due to Unix mecanism about creation date """

    def test_capatcha_object_is_valid(self):
        """ Test key validity """
        req = HttpRequest()
        req.user = AnonymousUser()
        req.session = SessionBase()
        cap = Capatcha(req)
        self.assertFalse(cap.isValid("acodetoolongtobevalid"))
