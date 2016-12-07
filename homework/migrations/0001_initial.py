# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-12-07 05:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userpage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xt_id', models.CharField(max_length=32)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CourseStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homework.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userpage.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xt_id', models.CharField(max_length=32)),
                ('title', models.TextField()),
                ('start_time', models.DateField()),
                ('end_time', models.DateField()),
                ('detail', models.TextField()),
                ('attachment', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homework.Course')),
            ],
        ),
        migrations.CreateModel(
            name='HomeworkStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted', models.BooleanField()),
                ('graded', models.BooleanField()),
                ('grading', models.TextField()),
                ('grading_comment', models.TextField()),
                ('graded_by', models.CharField(max_length=32)),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homework.Homework')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userpage.Student')),
            ],
        ),
    ]
