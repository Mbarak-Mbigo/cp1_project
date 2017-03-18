"""room module.

app/room.py

"""

# imports
from abc import ABCMeta, abstractmethod, abstractproperty

# local imports
from app.idgen import id_gen


class Room(object):
    """Docstring for Room abstract class."""

    # abstract class
    __metaclass__ = ABCMeta

    def __init__(self, name, type='OFFICE'):
        """Docstring for init."""
        self.id = id_gen()
        self.name = name
        self.type = type         # only accept office or living
        self.occupants = []

    def __str__(self):
        """Object string representation."""
        return "Id: " + str(self.id) + " Name: " + self.name + \
            " Type: " + self.type + '\n'

    @abstractmethod
    def is_full(self):
        """"Return true if full, false otherwise."""
        pass


class Office(Room):
    """Docstring for office."""

    # cls variables
    MAX_CAPACITY = 6
    rooms = 0

    def __init__(self, *args, **kwargs):
        """Initialize office instance varialbles."""
        self.occupants = []
        Office.rooms += 1
        super(Office, self).__init__(*args, **kwargs)

    def is_full(self):
        """Overide base implementation."""
        if len(self.occupants) < Office.MAX_CAPACITY:
            return True
        else:
            return False

    def __str__(self):
        """String representation."""
        return "Id: " + self.id + " Name: " + self.name + " Type: " +\
            self.type

    def __del__(self):
        """Update number of rooms after deleting."""
        Office.rooms -= 1


class Living(Room):
    """Subclass of Room."""

    # cls variables
    MAX_CAPACITY = 4
    rooms = 0

    def __init__(self, *args, **kwargs):
        """Initialize instance variables."""
        self.occupants = []
        Living.rooms += 1
        super(Living, self).__init__(*args, **kwargs)

    def is_full(self):
        """Overiding base implementation."""
        if len(self.occupants) < Living.MAX_CAPACITY:
            return True
        else:
            return False

    def __str__(self):
        """String representation."""
        return "Id: " + self.id + " Name: " + self.name + " Type: " +\
            self.type

    def __del__(self):
        """Update living rooms after deleting."""
        Living.rooms -= 1
