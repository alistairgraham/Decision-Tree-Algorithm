# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:08:39 2019

Decision Tree Algorithm

@author: Alistair Graham
"""

import sys
from random import randint

from tree import Node
from tree import LeafNode
from tree import Instance

# Fields
categories = []
attributes = []

trainingInstances = []
testInstances = []
global baseline
global baselineProbability


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
    
def buildTree(instances, currentAttributes):
    # if instances list is empty
    if not instances:
        return LeafNode(baseline, baselineProbability)
                
                
    # if instances are pure, return a leaf node
    trueList = []
    falseList = []
    for instance in instances:
        classifyCategory(instance, trueList, falseList)
    
    if not (trueList and falseList):
        return LeafNode(instance.attributeList[0], 1)
            
    # if attributes are empty, return a leaf node
    if not currentAttributes:
        if len(trueList) > len(falseList):
            return LeafNode(categories[0], (len(trueList)/len(instances)))
        elif len(trueList) < len(falseList):
            return LeafNode(categories[1], (len(falseList)/len(instances)))
        else:
            randomInt = randint(0,1)
            if (randomInt == 0):
                return LeafNode(categories[0], (len(trueList)/len(instances)))
            else:
                return LeafNode(categories[1], (len(falseList)/len(instances)))
    
    trueList = []
    falseList = []
    bestImpurity = 1.1
    bestAttributeIndex = 0
    #Finding purist attribute
    # i + 1 because instance.attributeList includes class at start
    for i, attribute in enumerate(currentAttributes):
        tempTrueList = []
        tempFalseList = []
        index = attributes.index(attribute)
        for instance in instances:
            # add the instance to true or false for the attribute
            if not isinstance(instance, Instance):
                raise TypeError
            if instance.attributeList[index+1] == "true":
                tempTrueList.append(instance)
            elif instance.attributeList[index+1] == "false":
                tempFalseList.append(instance)
            else:
                raise ValueError
            
        impurity = computeImpurity(tempTrueList, tempFalseList)
        if (impurity <= bestImpurity):
            bestImpurity = impurity
            trueList = tempTrueList
            falseList = tempFalseList
            bestAttributeIndex = i
    
    # Build subtrees
    unusedAttributes = currentAttributes[0:bestAttributeIndex] + currentAttributes[bestAttributeIndex+1:len(currentAttributes)]
    left = buildTree(trueList, unusedAttributes)
    right = buildTree(falseList, unusedAttributes)

    return Node(currentAttributes[bestAttributeIndex], left, right)
    
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
    
    numOfInstances = len(trueList) + len(falseList)
    impurityTrue = calculateImpurity(trueList) * (len(trueList) / numOfInstances)
    impurityFalse = calculateImpurity(falseList) * (len(falseList) / numOfInstances)
    return impurityTrue + impurityFalse

# calculate impurity of given instances
def calculateImpurity(branchInstances):
    
    outcome1 = 0
    outcome2 = 0
    
    for instance in branchInstances:
        if instance.attributeList[0] == categories[0]:
            outcome1 += 1
        elif instance.attributeList[0] == categories[1]:
            outcome2 += 1
        else:
            raise ValueError
    if len(branchInstances) == 0:
        return 0
    return ((outcome1/len(branchInstances)) * (outcome2/len(branchInstances)))
    
def classifyTestInstances(rootNode):
    correct = []
    incorrect = []
    for i, instance in enumerate(testInstances):
        classification = classify(instance, i, rootNode)
        if (classification == instance.attributeList[0]):
            correct.append(instance)
        else:
            incorrect.append(instance)

    print("DT Accuracy = " + str(len(correct)/len(testInstances)*100))
    
def classify(instance, instanceIndex, node):
    if isinstance(node, Node):
        attIndex = attributes.index(node.getAttribute)
        attributeForTest = testInstances[instanceIndex].attributeList[attIndex+1]
        if attributeForTest == "true":
            return classify(instance, instanceIndex, node._left)
        elif attributeForTest == "false":
            return classify(instance, instanceIndex, node._right)
        else:
            print(attributeForTest)
            raise ValueError
            
    elif isinstance(node, LeafNode):
        return node._classification
    else:
        raise TypeError
        
        
def computeBaseline():
    yes = []
    no = []
    classifyTraining(yes, no)
    
    global baseline
    global baselineProbability
    
    # Set baseline to most popular classification
    if len(no) < 1 and len(yes) < 1:
        raise ValueError
    if len(yes) > len(no):
        baseline = yes[0].attributeList[0]
        baselineProbability = len(yes)/len(trainingInstances)
    elif len(yes) <= len(no):
        baseline = no[0].attributeList[0]
        baselineProbability = len(no)/len(trainingInstances)
    else:
        raise ValueError
    
def classifyTraining(yesList, noList):
    for instance in trainingInstances:
        if instance.attributeList[0] == categories[0]:
            yesList.append(instance)
        elif instance.attributeList[0] == categories[1]:
            noList.append(instance)
        else:
            raise ValueError
            
def classifyUsingBaseline():
    correct = []
    
    for i, instance in enumerate(testInstances):
        if testInstances[i].attributeList[0] == baseline:
            correct.append(instance)
    
    print("Baseline Accuracy = " + str(len(correct)/len(testInstances)*100))
    
#def classifyTestInstances(rootNode):
    
    
    
    
def main():
    readFiles(sys.argv[1], sys.argv[2])
    print(testInstances[len(testInstances)-1].attributeList)
    print()
    computeBaseline()
    print(trainingInstances == trainingInstances.copy())
    rootNode = buildTree(trainingInstances.copy(), attributes.copy())
    rootNode.report("")
    classifyTestInstances(rootNode)
    classifyUsingBaseline()

main()









