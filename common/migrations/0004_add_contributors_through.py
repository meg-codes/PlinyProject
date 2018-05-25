# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-13 18:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_delete_contributors'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkContributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contribution_type', models.PositiveSmallIntegerField(choices=[(0, 'Author'), (1, 'Editor'), (2, 'Translator')])),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='contributor',
            name='contributor_type',
        ),
        migrations.RemoveField(
            model_name='contributor',
            name='order',
        ),
        migrations.AddField(
            model_name='workcontributor',
            name='contributor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Contributor'),
        ),
        migrations.AddField(
            model_name='workcontributor',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Work'),
        ),
        migrations.AddField(
            model_name='work',
            name='contributors',
            field=models.ManyToManyField(through='common.WorkContributor', to='common.Contributor'),
        ),
    ]
