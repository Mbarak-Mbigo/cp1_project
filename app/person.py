"""Person module.

app/person.py

"""

from abc import ABCMeta, abstractmethod

# local imports
from app.idgen import id_generator


class Person(metaclass=ABCMeta):
    """Docstring for class Person."""

    # abstract class

    def __init__(self, name, idcode=None, office_space=None):
        """Docstring for __init__."""
        self.id = idcode
        self.name = name.upper()
        self.office_space = office_space

    @property
    def id(self):
        """Id property."""
        return self._id

    @id.setter
    def id(self, idcode):
        if idcode:
            self._id = idcode
        else:
            self._id = id_generator()

    @abstractmethod
    def __str__(self):
        """String representation of object person."""


class Staff(Person):
    """Docstring for Staff."""

    def __init__(self, *args, **kwargs):
        """Docstring for Staff."""
        self.role = 'STAFF'
        super(Staff, self).__init__(*args, **kwargs)

    def __repr__(self):
        """Object representation format for Staff."""
        return '{0} (id:{1} name:{2} office:{3})'.format(self.role, self.id,
                                                         self.name,
                                                         self.office_space)

    def __str__(self):
        """String representation."""
        return str(self.id) + ' ' + self.name + ' ' + self.role


class Fellow(Person):
    """Docstring for Fellow."""

    def __init__(self, name, idcode=None, office_space=None,
                 accommodation='N', living_space=None):
        """Initialize instance variables."""
        self.role = 'FELLOW'
        self.accommodation = accommodation
        self.living_space = living_space
        super(Fellow, self).__init__(name, idcode, office_space)

    def __repr__(self):
        """Defining object representation."""
        return '{0} (id:{1} name:{2} office:{3} living:{4} '\
            'accommodation:{5}'.format(self.role, self.id, self.name,
                                       self.office_space, self.living_space,
                                       self.accommodation)

    def __str__(self):
        """String representation."""
        return str(self.id) + ' ' + self.name + ' ' + self.role + ' ' +\
            self.accommodation
