# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-12-13 12:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_work', models.BooleanField(default=True)),
                ('s_notice', models.BooleanField(default=True)),
                ('s_academic', models.BooleanField(default=True)),
                ('s_lecture', models.BooleanField(default=True)),
                ('s_class', models.BooleanField(default=True)),
                ('s_grading', models.BooleanField(default=True)),
                ('s_class_ahead_time', models.IntegerField(default=20)),
                ('s_ddl', models.BooleanField(default=True)),
                ('s_ddl_ahead_time', models.IntegerField(default=60)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_id', models.CharField(db_index=True, max_length=64, unique=True)),
                ('xt_id', models.CharField(db_index=True, max_length=32, null=True, unique=True)),
                ('pref', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='userpage.Preference')),
            ],
        ),
    ]