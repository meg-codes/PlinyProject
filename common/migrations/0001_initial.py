# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-16 18:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=191)),
                ('first_name', models.CharField(blank=True, max_length=191)),
                ('contributor_type', models.PositiveSmallIntegerField(choices=[(0, 'Author'), (1, 'Editor'), (2, 'Translator')])),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField()),
                ('title', models.TextField()),
                ('citation_override', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('work_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='common.Work')),
                ('volume', models.PositiveSmallIntegerField()),
                ('pages', models.CharField(max_length=30)),
                ('journal', models.CharField(max_length=191)),
                ('doi_or_url', models.TextField(blank=True)),
            ],
            bases=('common.work',),
        ),
        migrations.CreateModel(
            name='Monograph',
            fields=[
                ('work_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='common.Work')),
                ('place_of_publication', models.CharField(max_length=191)),
                ('publisher', models.CharField(max_length=191)),
            ],
            bases=('common.work',),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('work_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='common.Work')),
                ('pages', models.CharField(max_length=30)),
                ('contained_in', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cited_sections', to='common.Monograph')),
            ],
            bases=('common.work',),
        ),
        migrations.AddField(
            model_name='work',
            name='contributors',
            field=models.ManyToManyField(to='common.Contributor'),
        ),
    ]
