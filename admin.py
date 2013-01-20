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
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.conf import settings

from capatcha.models import Preference

class AdminImageWidget(AdminFileWidget):
    """ Affichage d'une miniature dans l'admin """
    def render(self, name, value, attrs=None):
        """ Rendu à la demande """
        output = []
        if value:
            output.append(u'<div>%s</div>' % (value))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        if value and getattr(value, "url", None):
            #l'image mais on pourrait aussi mettre un lien
            img = u'<div><img src="%s" width="128px"/></div>' % (value.url)
            output.append(img)
        return mark_safe(u''.join(output))

class AdminFontWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value:
            output.append(u'<div>%s</div>' % value)
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        if value and getattr(value, "url", None):
            text = u'''<style type="text/css">
            @font-face {
                src: url("%s%s");
                font-family: sample;
            }
            </style>
            <div style="font-family:sample; font-size: 48px;">Portez vieux ce whiskey au juge blond qui fume</div>
            ''' % (settings.MEDIA_URL, value)
            output.append(text)
        return mark_safe(u''.join(output))

class BaseAdmin(admin.ModelAdmin):
    """ Base pour tout les modules d'administration """
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'background':
            kwargs['widget'] = AdminImageWidget
            kwargs.pop('request', None) #erreur sinon
            return db_field.formfield(**kwargs)
        elif db_field.name == 'font':
            kwargs['widget'] = AdminFontWidget
            kwargs.pop('request', None)
            return db_field.formfield(**kwargs)
        return super(BaseAdmin, self).formfield_for_dbfield(db_field, **kwargs)


admin.site.register(Preference, BaseAdmin)
