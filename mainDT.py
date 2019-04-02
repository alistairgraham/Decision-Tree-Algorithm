# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:08:39 2019

Decision Tree Algorithm

@author: Alistair Graham
"""

import sys
import math

from tree import Node
from tree import LeafNode
from tree import Instance

# Fields
categories = []
attributes = []

trainingInstances = []
testInstances = []


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
        #print(trainingInstances)
        loadInstances(trainingFile, trainingInstances)
       # print(trainingInstances)
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
    # if instances list is empty
    if not instances:
        yes = []
        no = []
        for instance in instances:
            if instance.attributeList[0] == categories[1]:
                yes.append(instance)
            elif instance.attributeList[0] == categories[1]:
                no.append(instance)
            else:
                raise ValueError
        
        if len(yes) > len(no):
            return LeafNode(yes[0].attributeList[0], len(yes)/len(instances))
        else:
            return LeafNode(no[0].attributeList[0], len(no)/len(instances))
                
                
    # if instances are pure, return a leaf node
    trueList = []
    falseList = []
    for instance in instances:
        classifyCategory(instance, trueList, falseList)
        
    if not (trueList and falseList):
        #print(instance.attributeList[0])
        #print(trueList)
        return LeafNode(instance.attributeList[0], 1)
            
    # if attributes are empty, return a leaf node
    if not attributes:
        return LeafNode(categories[0], 1)
    
    trueList = []
    falseList = []
    bestImpurity = 1
    bestAttributeIndex = 0
    
    #Finding purist attribute
    # i + 1 because instance.attributeList includes class at start
    for i in range(1, len(attributes)+1):
        tempTrueList = []
        tempFalseList = []
        for instance in instances:
            # add the instance to true or false for the attribute
            if not isinstance(instance, Instance):
                raise TypeError
            if instance.attributeList[i] == "true":
                tempTrueList.append(instance)
            elif instance.attributeList[i] == "false":
                tempFalseList.append(instance)
            else:
                raise ValueError
            
            # todo: add weight
        impurity = computeImpurity(tempTrueList, tempFalseList)
        if (impurity < bestImpurity):
            bestImpurity = impurity
            trueList = tempTrueList
            falseList = tempFalseList
            bestAttributeIndex = i-1
                
    print(attributes[bestAttributeIndex])
    # Build subtrees
    unusedAttributes = attributes[0:bestAttributeIndex] + attributes[bestAttributeIndex:len(attributes)]
    left = buildTree(trueList, unusedAttributes)
    right = buildTree(falseList, unusedAttributes)

    return Node(attributes[bestAttributeIndex], left, right)
    
def classifyCategory(instance, trueList, falseList):
    if not isinstance(instance, Instance):
        raise TypeError
        
    if instance.attributeList[0] == categories[0]:
        trueList.append(instance)
    elif instance.attributeList[0] == categories[1]:
        falseList.append(instance)
    else:
        raise ValueError

def computeImpurity(trueList, falseList):
    truePureCount = 0
    trueImpureCount = 0
    impurityTrue = 1
    impurityFalse = 1
    
    for instance in trueList:
        if not isinstance(instance, Instance):
            raise TypeError
        if instance.attributeList[0] == categories[0]:
            truePureCount += 1
        elif instance.attributeList[0] == categories[1]:
            trueImpureCount += 1
        else:
            raise ValueError
        impurityTrue = (truePureCount*trueImpureCount)/(math.pow((truePureCount+trueImpureCount), 2))
    
    truePureCount = 0
    trueImpureCount = 0
    
    for instance in falseList:
        if not isinstance(instance, Instance):
            raise TypeError
        if instance.attributeList[0] == categories[0]:
            truePureCount += 1
        elif instance.attributeList[0] == categories[1]:
            trueImpureCount += 1
        else:
            raise ValueError
        impurityFalse = (truePureCount*trueImpureCount)/(math.pow((truePureCount+trueImpureCount), 2))
    
    # todo: needs to be weighted bro
    impurity = (impurityTrue+impurityFalse)/2
    return impurity
    
def classifyTestInstances():
    return


def main():
    readFiles(sys.argv[1], sys.argv[2])
    print(attributes)
    rootNode = buildTree(trainingInstances, attributes)
    classifyTestInstances()
    print(rootNode.attributeIndex)
    print(rootNode.left)
    print(rootNode.right)

main()









