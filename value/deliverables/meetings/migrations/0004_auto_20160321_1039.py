# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 08:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0001_initial'),
        ('factors', '0002_auto_20151014_2051'),
        ('meetings', '0003_auto_20151014_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='factors',
            field=models.ManyToManyField(related_name='meetings', to='factors.Factor'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='measure',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meetings', to='measures.Measure'),
        ),
    ]