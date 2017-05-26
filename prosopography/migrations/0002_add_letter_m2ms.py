# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0001_initial'),
        ('prosopography', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='correspondent',
            name='letters_to',
            field=models.ManyToManyField(related_name='letters_to', to='letters.Letter'),
        ),
        migrations.AddField(
            model_name='correspondent',
            name='mentioned_in',
            field=models.ManyToManyField(related_name='mentioned_in', to='letters.Letter'),
        ),
    ]
