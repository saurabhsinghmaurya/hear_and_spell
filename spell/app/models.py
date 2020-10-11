# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(db_index=True, max_length=200)
    email = models.CharField(db_index=True, max_length=200)
    password = models.CharField(db_index=True, max_length=35)
    start = models.IntegerField(default=0)
    test_id = models.IntegerField(default=-1)


class Test(models.Model):
    uid = models.IntegerField(db_index=True, default=-1)
    min_len = models.IntegerField(db_index=True)
    max_len = models.IntegerField(db_index=True)
    min_rank = models.IntegerField(db_index=True)
    max_rank = models.IntegerField(db_index=True)
    current_word_idx = models.IntegerField(default=0)
    total_words = models.IntegerField(default=0)
    completed = models.IntegerField(default=0)
    correct = models.IntegerField(db_index=True, default=0)
    wrong = models.IntegerField(db_index=True, default=0)


class WordInfo(models.Model):
    word = models.CharField(db_index=True, max_length=50)
    uid = models.IntegerField(db_index=True)
    correct = models.IntegerField(db_index=True, default=0)
    wrong = models.IntegerField(db_index=True, default=0)


class WordList(models.Model):
    word = models.CharField(db_index=True, max_length=50)
    length = models.IntegerField(default=0)
