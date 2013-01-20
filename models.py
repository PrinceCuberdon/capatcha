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
from django.db import models
from django.conf import settings

class Preference(models.Model):
    """ Definition des préférences pour le capatcha """
    charset = models.CharField(max_length=100, default="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", help_text="Jeux de caractère utilisé pour générer le capatcha", verbose_name="Jeux de caratères")
    size = models.SmallIntegerField(default=4, help_text=u"Taille par defaut du capatcha", verbose_name="Taille")
    font = models.FileField(upload_to=settings.CAPATCHA_CONFIG.Download, help_text=u"Police de caractère affichée", verbose_name="Police")
    background = models.ImageField(upload_to=settings.CAPATCHA_CONFIG.Download, help_text=u"Image de fond du capatcha", verbose_name="Image de fond")
    casesensitive = models.BooleanField(default=False, help_text=u"Est-ce que le capatcha est sensible aux majuscules et minuscules.", verbose_name=u"Sensible à la casse")

    def __unicode__(self):
        return u"Préférences"
