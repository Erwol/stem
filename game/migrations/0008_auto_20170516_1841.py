# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-16 18:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_question_attemps'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['-end_date'], 'verbose_name': 'Partida', 'verbose_name_plural': 'Partidas'},
        ),
        migrations.AlterModelOptions(
            name='useranswer',
            options={'verbose_name': 'Respuesta', 'verbose_name_plural': 'Respuestas'},
        ),
        migrations.AddField(
            model_name='game',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 16, 18, 40, 48, 516020), null=True, verbose_name='Fecha de modificación'),
        ),
        migrations.AddField(
            model_name='game',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Fecha de creación'),
            preserve_default=False,
        ),
    ]