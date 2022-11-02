#!/usr/bin/python3

from tracemalloc import start
import boto3
import csv
import sys
import time
import json
import botocore
import threading
import random

#
# usage: python3 updateentity.py <workspaceid> <root_entity_name> <child count> <region name>
#

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

if len(sys.argv) < 5:
    print ("please specify workspace_id, root_entity_name, child_count, region_name.")
    sys.exit()

class createChildThread (threading.Thread):
    def __init__(self, threadName, entityUtil, parent_entity_id, start_index):
        threading.Thread.__init__(self)
        self.name = threadName
        self.entityUtil = entityUtil
        self.parent_entity_id = parent_entity_id
        self.childcount = self.entityUtil.childcount
        self.start_index = start_index

    def run(self):
        print ("Starting Thread " + self.name)

        for entityindex in range(self.start_index, self.start_index+10):
            childentityname = "childentity-c-id-" + str(entityindex)
            rsp = self.entityUtil.iottwinmaker_client.create_entity(
                workspaceId=self.entityUtil.workspace_id,
                entityId = childentityname,
                entityName=childentityname,
                parentEntityId=self.entityUtil.parent_entity_id)
            childentityid = rsp["entityId"]
            print ("Thread [" + self.name + "]" + " created child entity id = " + childentityid)

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
        self.depth = 2
        print ("Create a tree with depth = " + str(self.depth) + ", " + str(self.childcount) + " child per parent.")
        rsp = self.iottwinmaker_client.create_entity(
            workspaceId=self.workspace_id,
            entityName=parent_entity_name)
        self.parent_entity_id = rsp["entityId"]
        
        #wait for parent entity to become active
        time.sleep(5)
        
        print ("Root entity created with id =" + self.parent_entity_id)

    def createEntitiesWithParent(self):
        
        # Wait for all threads complete
        threads = []
            
        for index in range(1, 11):
            
            startIndex = (index -1) * 10
            threadName = "CreateThread" + str(startIndex)

            # Create new threads
            thread = createChildThread(threadName, self, self.parent_entity_id, startIndex)

            # Start new Threads
            thread.start()
            
            # Add threads to thread list
            threads.append(thread)
        
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
rootEntityName =sys.argv[2]
childCount = int(sys.argv[3])
regionName = sys.argv[4]

et = EntityUtil(
    workspace_id=workspaceId,
    parent_entity_name=rootEntityName,
    child_count=childCount,
    region_name=regionName)
et.createEntitiesWithParent()
