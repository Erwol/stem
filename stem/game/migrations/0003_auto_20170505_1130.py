# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 11:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20170505_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='questions_number',
            field=models.IntegerField(default=0, editable=False, help_text='Número autogenerado de preguntas de una historia', null=True),
        ),
    ]