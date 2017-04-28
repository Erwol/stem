# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 14:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0006_auto_20170428_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextQuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('answer', models.TextField(verbose_name='Respuesta a la pregunta')),
            ],
            options={
                'verbose_name_plural': 'Preguntas de tipo texto',
                'verbose_name': 'Pregunta de tipo texto',
            },
        ),
        migrations.RemoveField(
            model_name='textquestion',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='question_text',
            field=models.TextField(default=1, verbose_name='Enunciado de la pregunta.'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='TextQuestion',
        ),
        migrations.AddField(
            model_name='textquestionanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question'),
        ),
    ]
