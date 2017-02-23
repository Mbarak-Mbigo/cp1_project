# app/room.py

# imports
from abc import ABCMeta, abstractmethod
class Room(object):
    
    #make room an abstract class
    __metaclass__ = ABCMeta
    
    OFFICE_MAX_CAPACITY = 6
    LIVING_SPACE_MAX_CAPACITY = 4
    total_office_space = 0
    total_living_space = 0
    def __init__(self, room_id=1, description=None, type=None):
        self.room_id = room_id
        self.type =type         # only accept office or living_space
        self.description = description
        self.spaces = []
    
    @staticmethod
    def add_office_space():
        pass
    
    @staticmethod
    def update_office_space():
        pass
    
    @staticmethod
    def add_living_space():
        pass
    
    @staticmethod
    def update_living_space():
        pass
    
    
    @abstractmethod
    def room_type(self):
        """"
        return the room type of room
        """
        
    def is_fully_occupied(self):
        pass
        """"return true if full and false otherwise"""
        
        
        