"""room module.

app/room.py

"""

# imports
from abc import ABCMeta, abstractmethod

# local imports
from app.idgen import id_generator


class Room(metaclass=ABCMeta):
    """Docstring for Room."""

    def __init__(self, name, idcode=None, occupants=None):
        """Initializing instance variables."""
        self.name = name.upper()
        self.id = idcode
        self.occupants = occupants

    # room id
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, code):
        if code:
            self._id = code
        else:
            self._id = id_generator()

    # room occupants
    @property
    def occupants(self,):
        return self._occupants

    @occupants.setter
    def occupants(self, occupants_list):
        if occupants_list:
            self._occupants = []
            self._occupants.extend(occupants_list)
        else:
            self._occupants = []

    @abstractmethod
    def is_full(self):
        """Return True if room fully occupied."""
        pass

    def __repr__(self):
        return 'Room(id:{0} name:{1} occupants:{2}'.format(
            self.id, self.name, self.occupants)


class Office(Room):
    """Docstring for office."""

    # cls variables
    MAX_CAPACITY = 6

    def __init__(self, *args, **kwargs):
        """Initialize office instance varialbles."""
        self.type_ = 'OFFICE'
        super(Office, self).__init__(*args, **kwargs)

    def is_full(self):
        """Overide base implementation."""
        if len(self.occupants) < Office.MAX_CAPACITY:
            return False
        else:
            return True

    def __str__(self):
        """String representation."""
        return str(Room.id) + ' ' + self.name + ' ' +\
            self.type_


class Living(Room):
    """Subclass of Room."""

    # cls variables
    MAX_CAPACITY = 4

    def __init__(self, *args, **kwargs):
        """Initialize instance variables."""
        self.type_ = 'LIVING'
        super(Living, self).__init__(*args, **kwargs)

    def is_full(self):
        """Overiding base implementation."""
        if len(self.occupants) < Living.MAX_CAPACITY:
            return False
        else:
            return True

    def __str__(self):
        """String representation."""
        return str(self.id) + ' ' + self.name + ' ' +\
            self.type_
