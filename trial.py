"""Project trial run.

trial.py
"""
# imports
# from app.amity import Amity

# from app.room import Office, Living
from app.person import Fellow, Staff

# office = Office('lala')
# print(office.__dict__)
# print(office.is_full())

# living = Living("sina")
# print(living.__dict__)
# print(living.is_full())

staff = Staff('am staff', 4444, 'myofficespace')
print(staff.__dict__)

fellow = Fellow('am fellow', 2222, None)
print(fellow.__dict__)

KELLY McGUIRE STAFF