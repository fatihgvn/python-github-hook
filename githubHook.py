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

    def addNewProject(self):
        
        if not os.path.exists(self.payloadFile): # if payload file is not found
            logger.info("create \"%s\" payload file" % (self.payloadFile))
            with open(self.payloadFile, 'w') as fp:
                json.dump(self.data, fp)    # create payload file

        hookBuff = None
        cloneRepo = False

        with open('hooks.json') as f:
            hooks = json.load(f)
            if not str(self.data['repository']['id']) in hooks: # if repo id is not defined in hooks.json
                cloneRepo = True
                tempDir = "/tmp/" + self.data['repository']['name']

                hooks[str(self.data['repository']['id'])] = tempDir   # add repo id
                
                self.repositoryFolder = tempDir

                hookBuff = hooks

                logger.info("add new hook \"%s\"" % (self.data['repository']['full_name']))

        with open('hooks.json', 'w') as fp:
            json.dump(hookBuff, fp)    # save repos
        
        if(cloneRepo):
            self.clone()

    def pull(self):
        try:
            
            if self.repositoryFolder != False:
                g = git.cmd.Git(self.repositoryFolder)
                g.pull()
                logger.info("%d id project updated in '%s' directory" % (self.data['repository']['id'], self.repositoryFolder))
            else:
                logger.error("%d The folder with id could not be found. please add this id to the 'hooks.json' file!" % (self.data['repository']['id']))

        except:
            logger.error("'%s' error pull request" % (self.repositoryFolder))
    

    def clone(self):
        try:
            
            if self.repositoryFolder != False:

                if not os.path.exists(self.repositoryFolder):
                    os.makedirs(self.repositoryFolder)

                git.Repo.clone_from(self.data['repository']['git_url'], self.repositoryFolder)

                logger.info("%d id project cloned in '%s' directory" % (self.data['repository']['id'], self.repositoryFolder))
            else:
                logger.error("%d The folder with id could not be found. please add this id to the 'hooks.json' file!" % (self.data['repository']['id']))

        except:
            logger.error("'%s' error clone request" % (self.repositoryFolder))