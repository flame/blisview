# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 19:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('options_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='graph.Attribute')),
            ],
        ),
    ]