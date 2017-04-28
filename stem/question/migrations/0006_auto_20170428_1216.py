# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0005_auto_20170428_1142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textquestionanswer',
            name='question',
        ),
        migrations.RenameField(
            model_name='textquestion',
            old_name='text',
            new_name='question_text',
        ),
        migrations.AddField(
            model_name='textquestion',
            name='answer',
            field=models.TextField(default=1, verbose_name='Respuesta a la pregunta'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='TextQuestionAnswer',
        ),
    ]
