# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

from django.apps import AppConfig
from django.contrib.staticfiles.storage import staticfiles_storage

from .models import WordList


EN_HI_DICT = None
WORDS_LIST_INIT = False
EN_HI_DICT_FILE = 'en_hi.json'
WORDS_LIST_FILE = '20k.txt'

class SpellConfig(AppConfig):
    name = 'app'
    def ready(self):
        # put your startup code here
        #link = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt"
        if EN_HI_DICT is None:
            self.load_dict()
        if WORDS_LIST_INIT is False:
            self.load_words()

    def load_words(self):
        """
        load words to sqlite from static file
        """
        global WORDS_LIST_INIT
        file_path = staticfiles_storage.path(WORDS_LIST_FILE)
        # Using readlines()
        fp = open(file_path, 'r')
        lines = fp.readlines()
        for line in lines:
            line = line.decode().strip()
            word = WordList.objects.create(word=line, length=line.__len__())
            word.save()
        fp.close()
        WORDS_LIST_INIT = True

    def load_dict(self):
        """
        load EN-HI dict from static file
        """
        global EN_HI_DICT
        logging.info("loading en-hi dict file")
        file_path = staticfiles_storage.path(EN_HI_DICT_FILE)
        fp = open(file_path)
        EN_HI_DICT = json.load(fp)
        fp.close()
