# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-10-29 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_catinfo_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='isShow',
            field=models.BooleanField(default=True, verbose_name='是否展示'),
        ),
    ]