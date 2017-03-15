# app/Persons.py

from abc import ABCMeta, abstractmethod


class Person(object):
    
    __metaclass__ = ABCMeta
    
    def __init__(self, name, type):
        self.id = id(self)
        self.name = name
        self.type = type
        self.office_space=None

    def __str__(self):
        return "Person Id: " + str(self.id) + " Name: " + self.name + " Type: " + self.type 


class Staff(Person):
    """docstring for Staff"""
    persons = 0
    def __init__(self, *args, **kwargs):
        Staff.persons += 1
        super(Staff, self).__init__(*args, **kwargs)

    def __del__(self):
        Staff.persons -= 1


class Fellow(Person):
    """docstring for Fellow"""
    persons = 0
    def __init__(self, *args, **kwargs):
        self.livingspace = None
        Fellow.persons += 1
        super(Fellow, self).__init__(*args, **kwargs)

    def __del__(self):
        Fellow.persons -= 1

        
