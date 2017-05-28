# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-28 23:19
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_textquestionanswer_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textquestionanswer',
            name='content',
        ),
        migrations.AddField(
            model_name='question',
            name='content',
            field=ckeditor.fields.RichTextField(default=1, verbose_name='Enunciado enriquecido test'),
            preserve_default=False,
        ),
    ]
