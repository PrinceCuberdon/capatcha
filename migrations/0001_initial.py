# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('charset', models.CharField(default=b'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', help_text=b'Jeux de caract\xc3\xa8re utilis\xc3\xa9 pour g\xc3\xa9n\xc3\xa9rer le capatcha', max_length=100, verbose_name=b'Jeux de carat\xc3\xa8res')),
                ('size', models.SmallIntegerField(default=4, help_text='Taille par defaut du capatcha', verbose_name=b'Taille')),
                ('font', models.FileField(help_text='Police de caract\xe8re affich\xe9e', upload_to=b'capatcha', verbose_name=b'Police')),
                ('background', models.ImageField(help_text='Image de fond du capatcha', upload_to=b'capatcha', verbose_name=b'Image de fond')),
                ('casesensitive', models.BooleanField(default=False, help_text='Est-ce que le capatcha est sensible aux majuscules et minuscules.', verbose_name='Sensible \xe0 la casse')),
            ],
        ),
    ]
