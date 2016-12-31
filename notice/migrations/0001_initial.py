# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-31 21:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userpage', '0001_initial'),
        ('homework', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xt_id', models.CharField(default=None, max_length=32)),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('publisher', models.CharField(max_length=32)),
                ('publishtime', models.DateField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homework.Course')),
            ],
        ),
        migrations.CreateModel(
            name='NoticeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False)),
                ('notice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notice.Notice')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userpage.Student')),
            ],
        ),
    ]
