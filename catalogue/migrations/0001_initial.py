# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=250, verbose_name=b'name', blank=True)),
                ('slug', models.SlugField(unique=True, max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.PositiveIntegerField(verbose_name=b'rate')),
                ('text', models.CharField(max_length=300, null=True, verbose_name=b'text', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(max_length=50)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(default=b'', verbose_name=b'Text')),
                ('upload_date', models.DateTimeField(verbose_name=b'Upload Date')),
                ('employee', models.ForeignKey(related_name='task_employee', blank=True, to='catalogue.MyUser', null=True)),
                ('employer', models.ForeignKey(related_name='task_employer', to='catalogue.MyUser')),
            ],
        ),
        migrations.CreateModel(
            name='TaskRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('employee', models.ForeignKey(to='catalogue.MyUser')),
                ('task', models.ForeignKey(to='catalogue.Task')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='employee',
            field=models.ForeignKey(related_name='comment_employee', verbose_name=b'employee', to='catalogue.MyUser'),
        ),
        migrations.AddField(
            model_name='comment',
            name='employer',
            field=models.ForeignKey(related_name='comment_employer', verbose_name=b'employer', to='catalogue.MyUser'),
        ),
    ]
