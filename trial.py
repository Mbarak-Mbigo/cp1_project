"""Project trial run.

trial.py
"""
# imports
from app.amity import Amity

from app.room import Room, Office, Living
from app.person import Person, Fellow, Staff

room = Room("Mida")
print(room)
amity = Amity()
amity.create_room("mida", "mdadf")
