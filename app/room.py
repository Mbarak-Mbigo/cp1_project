"""room module.

app/room.py

"""

# imports
from abc import ABCMeta, abstractmethod


class Room(object):
    """docstring for Room abstract class."""

    __metaclass__ = ABCMeta

    def __init__(self, name, type):
        self.room_id = id(self)
        self.name = name
        self.type =type         # only accept office or living
        self.occupants = []

    def __str__(self):
        return "Room Id: " + str(self.room_id) + " Name: " + self.name + " Type:" + self.type + '\n'
           
    def is_fully_occupied(self):
        """"return true if full and false otherwise"""
        pass

class office(Room):
    """docstring for office"""
    MAX_CAPACITY = 6
    rooms = 0
    def __init__(self, *args, **kwargs):
        self.occupants = []
        office.rooms += 1
        super(office, self).__init__(*args, **kwargs)

    def is_fully_occupied(self):
        if len(self.occupants) < MAX_CAPACITY:
            return True
        else:
            return False

    def __del__(self):
        office.rooms -= 1

class livingSpace(Room):
    """docstring for livingSpace"""
    MAX_CAPACITY = 4
    rooms = 0
    def __init__(self, *args, **kwargs):
        self.occupants = []
        livingSpace.rooms += 1
        super(livingSpace, self).__init__(*args, **kwargs)

    def is_fully_occupied(self):
        if len(self.occupants) < MAX_CAPACITY:
            return True
        else:
            return False

    def __del__(self):
        livingSpace.rooms -= 1
        
        
        
        