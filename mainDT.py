# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:08:39 2019

Decision Tree Algorithm

@author: Alistair Graham
"""

import sys
from tree import Node
from tree import Instance

# Fields
categories = []
attributes = []

trainingInstances = []
testInstances = []
rootNode = Node()


def readFiles(trainingFileName, testFileName):
    with open(trainingFileName) as trainingFile:
        # get categories
        line = trainingFile.readline()
        for word in line.split():
            categories.append(word)
        # get attributes
        line = trainingFile.readline()
        for word in line.split():
            attributes.append(word)            
            
        loadInstances(trainingFile, trainingInstances)
    
    with open(testFileName) as testFile:
        # skip headers
        testFile.readline()
        testFile.readline()
        loadInstances(testFile, testInstances)

def loadInstances(file, instancesList):
    for line in file.readlines():
        if len(line) <= 1:
            continue
        instancesList.append(Instance(line.split()))
    
def buildTree(instances, attributes):
    trueList = []
    falseList = []
    
    # Need to change to for each attribute
    #Finding best attribute
    for attribute in attributes:
        
            
        if instance.attributeList[0] == categories[0]:
            trueList.append(instance)
        else:
            falseList.append(instance)
    
    #purity = computePurity(trueList, falseList)

    return Node()
    
def classifyTestInstances():
    return


def main():
    readFiles(sys.argv[1], sys.argv[2])    
    rootNode = buildTree(trainingInstances, attributes)
    classifyTestInstances()    

main()










