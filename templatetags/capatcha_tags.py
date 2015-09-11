# -*- coding: UTF-8 -*-
# capatcha is part of Band Cochon
# Band Cochon (c) Prince Cuberdon 2011 and Later <princecuberdon@bandcochon.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Tags django pour le capatcha

Utilisation : 
{%load capatcha_tags%}
{%create_capatcha%}
<img src="{{capacha.path}}" />

une variable de session request.session['capatcha'] est mise sur l'objet capatcha défini ci-dessous
par consequence, l'objet request doit être passé dans la vue.

Caution : capatcha.path MUST be in a block due to Django limitation
"""

import random
import sys
import time
import datetime

import os
from PIL import Image, ImageDraw, ImageFont
from django import template
from django.conf import settings

from capatcha.models import Preference

register = template.Library()


class Capatcha(object):
    def __init__(self, request):
        self.removeOld()
        
        try:
            pref = Preference.objects.get(id=1)
        except:
            raise Exception(u"Preferences are not set")
        
        request.session['capatcha'] = self
        
        random.seed(os.urandom(10))
        code = ''.join([random.choice(pref.charset) for unused_i in xrange(pref.size)])
        img = Image.open(pref.background.path)
        width, height = img.size
        font = ImageFont.truetype(pref.font.path, 42)
        draw = ImageDraw.Draw(img)
        fwidth, fheight = draw.textsize(code, font=font)
        draw.text(((width - fwidth) / 2, (height - fheight) / 2), code, fill='#000000', font=font)
        imgrelpath = os.path.join(settings.MEDIA_URL, settings.CAPATCHA_CONFIG.temp, '%s.png' % request.session._get_session_key())
        if sys.platform == 'win32':
            imgrelpath = imgrelpath.replace("\\", '/')
        img.save("%s%s" % (settings.PROJECT_PATH, imgrelpath), 'PNG')

        self.key = code
        self.path = imgrelpath
        self.casesensitive = pref.casesensitive

    def isValid(self, value):
        """ Test captcha validity. calls from controler """
        try:
            if not self.casesensitive:
                value = value.lower()
                self.key = self.key.lower()
            return self.key == value
        except:
            pass
        
        return False
        
    def removeOld(self):
        """ Remove all capatcha where date stamp is < as today """
        rootpath = os.path.join(settings.MEDIA_ROOT,settings.CAPATCHA_CONFIG.temp)
        for current_file in os.listdir(rootpath):
            unused_name, ext = os.path.splitext(current_file)
            if not ext == '.png':
                continue
            f = os.path.join(rootpath, current_file)
            today_date = datetime.datetime.fromtimestamp(time.time())
            today_date = datetime.datetime(today_date.year, today_date.month, today_date.day)
            
            file_date = datetime.datetime.fromtimestamp(os.path.getctime(f))
            file_date = datetime.datetime(file_date.year, file_date.month, file_date.day)
            
            if file_date < today_date:
                try:
                    os.remove(f)
                except:
                    pass

class CapatchaNode(template.Node):
    def render(self, context):
        context['capatcha'] = Capatcha(context['request']) # Pour la vue
        context['request'].session['capatcha'] = context['capatcha'] # Pour le controler
        return ''

@register.tag
def create_capatcha(parser, token):
    """ Création d'un capatcha (voir __doc__)"""
    return CapatchaNode()

