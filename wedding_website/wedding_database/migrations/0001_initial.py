# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=30)),
                ('num_invited', models.IntegerField()),
                ('confirmed', models.BooleanField(default=False)),
                ('num_coming', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Invitee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('confirmed', models.BooleanField(default=False)),
                ('group', models.ForeignKey(to='wedding_database.Group')),
            ],
        ),
    ]
