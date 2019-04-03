# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:34:53 2019

@author: Alistair Graham
"""

class Node:
    
    def __init__(self, attribute, left, right):
        self._attribute = attribute
        self._left = left
        self._right = right
        
    def report(self, indent):
        print(indent + self._attribute + " = True:")
        self._left.report(indent+"    ");
        print(indent + self._attribute + " = False:")
        self._right.report(indent+"    ");
        
    @property
    def getAttribute(self):
        return self._attribute
        
        
class LeafNode:
    
    def __init__(self, classification, probability):
        self._classification = classification
        self._probability = probability
        
    def report(self, indent):
        print(str(indent) + "Class " + str(self._classification) + ", prob = " + "{0:.2f}".format(self._probability))

class Instance:
    
    def __init__(self, attributes):
        self._attributes = attributes
        return
    
    @property
    def attributeList(self):
        return self._attributes