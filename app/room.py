"""room module.

app/room.py

"""

# imports
from abc import ABCMeta, abstractmethod

# local imports
from app.idgen import id_gen


class Room(metaclass=ABCMeta):
    """Docstring for Room."""

    def __init__(self, name, type='OFFICE'):
        """Initializing instance variables."""
        super(Room, self).__init__()
        self.id = id_gen()
        self.name = name.title()
        self.type = type.upper()
        self.occupants = []

    @abstractmethod
    def is_full(self):
        """Return True if room fully occupied."""
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
        super(Office, self).__init__(type='OFFICE', *args, **kwargs)

    def is_full(self):
        """Overide base implementation."""
        if len(self.occupants) < Office.MAX_CAPACITY:
            return False
        else:
            return True

    def __str__(self):
        """String representation."""
        return "Id: " + str(self.id) + " Name: " + self.name + " Type: " +\
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
        Room.type = 'LIVING'
        self.occupants = []
        Living.rooms += 1
        super(Living, self).__init__(type='LIVING', *args, **kwargs)

    def is_full(self):
        """Overiding base implementation."""
        if len(self.occupants) < Living.MAX_CAPACITY:
            return False
        else:
            return True

    def __str__(self):
        """String representation."""
        return "Id: " + str(self.id) + " Name: " + self.name + " Type: " +\
            self.type

    def __del__(self):
        """Update living rooms after deleting."""
        Living.rooms -= 1
