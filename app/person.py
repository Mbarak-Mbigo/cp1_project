"""Person module.

app/person.py

"""

from abc import ABCMeta

# local imports
from app.idgen import id_gen


class Person(object):
    """Docstring for class Person."""

    # abstract class
    __metaclass__ = ABCMeta

    def __init__(self, name, type='FELLOW'):
        """Docstring for __init__."""
        self.id = id_gen()
        self.name = name
        self.type = type
        self.office_space = None

    def __str__(self):
        """Docstring for str."""
        return "Id: " + str(self.id) + " Name: " + \
            self.name + " Type: " + self.type

    def allocated_office(self):
        """Return true if allocated."""
        if self.office_space:
            return True
        else:
            return False


class Staff(Person):
    """Docstring for Staff."""

    persons = 0

    def __init__(self, *args, **kwargs):
        """Docstring for Staff."""
        Staff.persons += 1
        super(Staff, self).__init__(*args, **kwargs)

    def __str__(self):
        """String representation."""
        return "Id: " + self.id + " Name: " + self.name + " Type: " +\
            self.type

    def __del__(self):
        """Docstring for del."""
        Staff.persons -= 1


class Fellow(Person):
    """Docstring for Fellow."""

    persons = 0

    def __init__(self, wants_accommodation, *args, **kwargs):
        """Initialize instance variables."""
        self.accommodation = wants_accommodation
        self.living_space = None
        Fellow.persons += 1
        super(Fellow, self).__init__(*args, **kwargs)

    def __str__(self):
        """String representation."""
        return "Id: " + self.id + " Name: " + self.name + " Type: " +\
            self.type + ' ' + self.accommodation

    def __del__(self):
        """Update number of fellows after deleting."""
        Fellow.persons -= 1
