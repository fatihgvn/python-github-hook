#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple
import json, os
from logger import logger

class githubHook():
    PAYLOAD     = 0
    PUSH        = 1

    def __init__(self, data):
        self.data = data
        if data['zen']:
            self.event = self.PAYLOAD
        else:
            self.event = self.PUSH

        currentDirectory = os.getcwd() # get current directory
        self.payloadDir = currentDirectory + "/payloads" # payload folder

        if os.path.exists(self.payloadDir) and os.access(self.payloadDir, os.R_OK) and os.access(self.payloadDir, os.W_OK):

            self.payloadFile = currentDirectory + "/payloads/"+str(data['repository']['id'])+".json" # payload file

        else:
            logger.error("'%s' directory not found or is not readable" % (self.payloadDir))


        