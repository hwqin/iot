#!/usr/bin/python3

import boto3
import csv
import sys
import time
import json
import botocore
import threading
import random

#
# usage: python3 cleanupentity.py <workspaceid> <region name>
#

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

if len(sys.argv) < 3:
    print ("please specify workspace_id, region_name.")
    sys.exit()

class deleteEntityThread (threading.Thread):
    def __init__(self, threadName, entityUtil):
        threading.Thread.__init__(self)
        self.name = threadName+"Delete"
        self.entityUtil = entityUtil

    def run(self):
        print ("Starting Thread " + self.name)

        response = self.entityUtil.iottwinmaker_client.list_entities(
            workspaceId=self.entityUtil.workspace_id
        )
        entityList = response["entitySummaries"]

        for entityObject in entityList:
            entityId = entityObject["entityId"]
            rsp = self.entityUtil.iottwinmaker_client.delete_entity(
                workspaceId=self.entityUtil.workspace_id,
                isRecursive=True,
                entityId = entityId)
            print ("Thread [" + self.name + "]" + " delete child entity id = " + entityId)

        print ("Exiting Thread " + self.name)

class updateChildThread (threading.Thread):
    def __init__(self, threadName, entityUtil, parent_entity_id, index):
        threading.Thread.__init__(self)
        self.name = threadName
        self.entityUtil = entityUtil
        self.parent_entity_id = parent_entity_id
        self.index = index

    def run(self):
        print ("Starting Thread " + self.name)
        # Wait for all threads complete
        threads = []
        for entityindex in range(self.index+1, self.index+11):
            childentityid = "childentity-id-" + str(entityindex)
            rsp = self.entityUtil.iottwinmaker_client.update_entity(
                workspaceId=self.entityUtil.workspace_id,
                entityId = childentityid,
                parentEntityUpdate={
                    'parentEntityId': self.parent_entity_id,
                    'updateType': 'UPDATE'
                })
            print(rsp)
            print ("Thread [" + self.name + "]" + " update child entity id = " + childentityid)

        # Wait for all threads to complete
        for t in threads:
            t.join()

        print ("Exiting Thread " + self.name)

class EntityUtil():
    def __init__(self, workspace_id, parent_entity_name, child_count, region_name, profile=None):
        self.session = boto3.session.Session(profile_name=profile)
        #self.iottwinmaker_client = self.session.client(service_name='iottwinmaker', endpoint_url='https://gamma.us-east-1.twinmaker.iot.aws.dev')
        self.iottwinmaker_client = self.session.client(service_name='iottwinmaker', region_name=region_name)
        self.workspace_id = workspace_id
        self.childcount = child_count

    def deleteAllEntities(self):
        # Create new threads
        thread1 = deleteEntityThread("Thread", self)

        # Start new Threads
        thread1.start()

        # Wait for all threads complete
        threads = []
        # Add threads to thread list
        threads.append(thread1)
        
        # Wait for all threads to complete
        for t in threads:
            t.join()

    def attachParentEntityId(self):
        
        # Wait for all threads complete
        threads = []
        
        # Create new threads
        for utindex in range(1, 10) :
            childentityindex = (utindex - 1) * 10
            threadname = "ThreadU" + str(utindex)
            threadi = updateChildThread(threadname, self, self.parent_entity_id, childentityindex)
            threadi.start()
        
            # Add threads to thread list
            threads.append(threadi)

        # Wait for all threads to complete
        for t in threads:
            t.join()


# Create N depth level of tree, each parent has M child
# workspace_id, root_entity_name, tree_depth, child_count, region_name
workspaceId = sys.argv[1]
regionName = sys.argv[2]

et = EntityUtil(
    workspace_id=workspaceId,
    parent_entity_name="",
    child_count=0,
    region_name=regionName)
et.deleteAllEntities()
