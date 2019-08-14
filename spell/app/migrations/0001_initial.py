# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.IntegerField(default=-1, db_index=True)),
                ('min_len', models.IntegerField(db_index=True)),
                ('max_len', models.IntegerField(db_index=True)),
                ('min_rank', models.IntegerField(db_index=True)),
                ('max_rank', models.IntegerField(db_index=True)),
                ('correct', models.IntegerField(default=0, db_index=True)),
                ('wrong', models.IntegerField(default=0, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('email', models.CharField(max_length=200, db_index=True)),
                ('password', models.CharField(max_length=35, db_index=True)),
                ('start', models.IntegerField(default=0)),
                ('test_id', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='WordInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.IntegerField(db_index=True)),
                ('uid', models.IntegerField(db_index=True)),
                ('correct', models.IntegerField(default=0, db_index=True)),
                ('wrong', models.IntegerField(default=0, db_index=True)),
                ('correct_after_last_wrong', models.IntegerField(default=0, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='WordList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(max_length=50, db_index=True)),
                ('length', models.IntegerField(default=0)),
            ],
        ),
    ]
