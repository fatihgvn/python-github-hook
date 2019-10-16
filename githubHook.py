#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple
import json, os
from logger import logger
import git

class githubHook():
    PAYLOAD     = 0
    PUSH        = 1

    def __init__(self, data):
        self.data = data
        if 'zen' in data:
            self.event = self.PAYLOAD
        else:
            self.event = self.PUSH

        currentDirectory = os.getcwd() # get current directory
        self.payloadDir = currentDirectory + "/payloads" # payload folder

        if os.path.exists(self.payloadDir) and os.access(self.payloadDir, os.R_OK) and os.access(self.payloadDir, os.W_OK):

            self.payloadFile = currentDirectory + "/payloads/"+str(self.data['repository']['id'])+".json" # payload file
            with open('hooks.json') as f:
                hooks = json.load(f)
                if str(self.data['repository']['id']) in hooks:
                    self.repositoryFolder = hooks[str(self.data['repository']['id'])]
                else:
                    self.repositoryFolder = False

        else:
            logger.error("'%s' directory not found or is not readable" % (self.payloadDir))

    def clone(self):
        try:
            
            if self.repositoryFolder != False:
                print("%d id project updated in '%s' directory" % (self.data['repository']['id'], self.repositoryFolder))
                g = git.cmd.Git(self.repositoryFolder)
                g.pull()
                logger.info("%d id project updated in '%s' directory" % (self.data['repository']['id'], self.repositoryFolder))
            else:
                logger.error("%d The folder with id could not be found. please add this id to the 'hooks.json' file!" % (self.data['repository']['id']))

        except:
            logger.error("'%s' error pull request" % (self.repositoryFolder))