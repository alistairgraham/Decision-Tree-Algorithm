# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:34:53 2019

@author: Alistair Graham
"""

class Node:
    
    def __init__(self):
        return
        

class Instance:
    
    def __init__(self, attributes):
        self._attributes = attributes
        return
    
    @property
    def attributeList(self):
        return self._attributes