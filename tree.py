# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:34:53 2019

@author: Alistair Graham
"""

class Node:
    
    def __init__(self, attributeIndex, left, right):
        self.attributeIndex = attributeIndex
        self.left = left
        self.right = right
        
class LeafNode:
    
    def __init__(self, classification, probability):
        self.classification = classification
        self.probability = probability

class Instance:
    
    def __init__(self, attributes):
        self._attributes = attributes
        return
    
    @property
    def attributeList(self):
        return self._attributes