"""Project trial run.

trial.py
"""
# imports
from app.amity import Amity

from app.room import Room, Office, Living
from app.person import Person, Fellow, Staff


amity = Amity()
# create offices
# amity.create_room(['Mida', 'Swift', 'Latifa'], 'office')
# amity.create_room(['myOffice'])
# # create staff
# amity.add_person('Mbarak Mbigo', 'STAFF')

# amity.load_people()
# amity.print_unallocated('data/unallocated.txt')
# amity.print_available_space()
amity.load_state('databases/default.db')
