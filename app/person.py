# app/Persons.py

from abc import ABCMeta, abstractmethod


class Person(object):
    
    __metaclass__ = ABCMeta
    
    def __init__(self, name, type):
        self.id = id(self)
        self.name = name
        self.type=  type
        self.office_space=None


class Staff(Person):
    """docstring for Staff"""
    staff = 0
    def __init__(self, *args, **kwargs):
        super(Staff, self).__init__(*args, **kwargs)


class Fellow(Person):
    """docstring for Fellow"""
    fellows = 0
    def __init__(self, *args, **kwargs):
        self.livingspace = None
        super(Fellow, self).__init__(*args, **kwargs)

        
