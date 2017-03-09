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

    def __str__(self):
        return "Room Id: " + str(self.room_id) + " Name: " + self.name + " Type:" + self.type + '\n'
           
    def is_fully_occupied(self):
        pass
        """"return true if full and false otherwise"""

class Office(Room):
    """docstring for Office"""
    MAX_CAPACITY = 6
    rooms = 0
    def __init__(self, *args, **kwargs):
        self.occupants = []
        Office.rooms += 1
        super(Office, self).__init__(*args, **kwargs)

    def __del__(self):
        Office.rooms -= 1

class LivingSpace(Room):
    """docstring for LivingSpace"""
    MAX_CAPACITY = 4
    rooms = 0
    def __init__(self, *args, **kwargs):
        self.occupants = []
        LivingSpace.rooms += 1
        super(LivingSpace, self).__init__(*args, **kwargs)

    def __del__(self):
        LivingSpace.rooms -= 1
        
        
        
        