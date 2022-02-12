# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

from django.apps import AppConfig
from django.contrib.staticfiles.storage import staticfiles_storage


EN_HI_DICT = None
EN_HI_DICT_FILE = 'en_hi.json'

class SpellConfig(AppConfig):
    name = 'app'
    def ready(self):
        # put your startup code here
        if EN_HI_DICT is None:
            self.load_dict()

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
