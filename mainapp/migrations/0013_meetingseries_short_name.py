# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingseries',
            name='short_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
