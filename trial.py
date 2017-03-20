"""Project trial run.

trial.py
"""
# imports
from app.amity import Amity

from app.room import Room, Office, Living
from app.person import Person, Fellow, Staff


amity = Amity()
# create offices
amity.create_room(['Mida', 'Swift', 'Latifa'], 'office')
# amity.create_room(['myOffice'])
# create staff
print(amity.add_person('Mrichiwa', 'STAFF'))
# print(amity.add_person('Mbarak Mbigo', 'STAFF'))
print(amity.persons['staff']['Mrichiwa'])

print(amity.load_people())
print(amity.persons)
print(amity.print_allocations())
print(amity.print_unallocated())
print(amity.print_room('Latifa'))
