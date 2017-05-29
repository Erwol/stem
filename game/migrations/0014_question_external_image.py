# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-29 02:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_remove_question_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='external_image',
            field=models.CharField(blank=True, help_text='Heroku elimina todos los archivos subidos x tiempo', max_length=512, verbose_name='Enlace a la imagen'),
        ),
    ]