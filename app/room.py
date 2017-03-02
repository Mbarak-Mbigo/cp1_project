# app/room.py

# imports
from abc import ABCMeta, abstractmethod


class Room(object):
    """docstring for Room
        abstract class 
    """
    __metaclass__ = ABCMeta
    
    def __init__(self, name, type):
        self.room_id = id(self)
        self.name = name
        self.type =type         # only accept Office or Living Space
        self.occupants = []
           
    def is_fully_occupied(self):
        pass
        """"return true if full and false otherwise"""

class Office(Room):
    """docstring for Office"""
    MAX_CAPACITY = 6
    def __init__(self, *args, **kwargs):
        self.occupants = []
        super(Office, self).__init__(*args, **kwargs)

class LivingSpace(Room):
    """docstring for LivingSpace"""
    def __init__(self, *args, **kwargs):
        self.occupants = []
        super(LivingSpace, self).__init__(*args, **kwargs)
        
        
        
        