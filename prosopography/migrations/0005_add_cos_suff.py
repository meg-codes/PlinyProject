# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-17 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosopography', '0004_add_citations'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='cos_suff',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
