"""Amity test suite.

tests/test.py

Process:
    Write a failing unit test
    Make the unit test pass
    Refactor
"""
# imports
import unittest
import unittest.mock

# local imports
from app.amity import Amity
from app.room import Room, Office, Living
from app.person import Person


class AmityTests(unittest.TestCase):
    """Test Suite for Amity."""

    # fixtures
    def setUp(self):
        """Create necessary objects."""
        self.amity = Amity()

    def tearDown(self):
        """Create necessary objects."""
        del self.amity

    def test_creates_room(self):
        """Test rooms are created successfully."""
        # Cannot create rooms with abstract class Room
        with self.assertRaises(TypeError):
            Room("Mida")
        # captures invalid input
        # Room type
        self.amity.create_room(["Mida"], "Other_type")
        self.assertNotIn("Mida", self.amity.rooms['offices'].keys() or
                         self.amity.rooms['livingspaces'].keys())
        # Room name not string
        self.amity.create_room(["Mambrui", 334])
        self.assertTrue(334 not in self.amity.rooms['offices'].keys())
        # Can create one room
        self.amity.create_room(['Narnia'], 'OFFICE')
        self.assertTrue('NARNIA' in self.amity.rooms['offices'].keys())
        # Does not allow to create room(s) already existing
        self.amity.create_room(['Narnia'], 'OFFICE')
        self.assertEqual('Room(s) Narnia already exists',
                         self.amity.create_room(['Narnia'], 'OFFICE'))

        # Can create many rooms
        num_of_rooms = (len(self.amity.rooms['livingspaces'].keys()))
        self.amity.create_room(['Tsavo', 'Zimmer'], 'LIVING')
        num_of_rooms_after = (len(self.amity.rooms['livingspaces'].keys()))
        self.assertGreater(num_of_rooms_after, num_of_rooms,
                           msg='Rooms should increase')
        self.assertEqual(num_of_rooms + 2, num_of_rooms_after,
                         msg='Rooms added should be equal to rooms created')

    def test_add_person(self):
        """Test add person functionallity."""
        # test rejects creating person with abstract class
        with self.assertRaises(TypeError):
            Person('Ramadhan Salim')
        # test adds succesfully
        self.amity.add_person('Jackson Nania', 'FELLOW')
        self.assertTrue('JACKSON NANIA' in
                        self.amity.persons['fellows'].keys())

        self.amity.add_person('Rehema Tanya', 'STAFF')
        self.assertTrue('REHEMA TANYA' in self.amity.persons['staff'].keys())

        # Test rejects duplicate
        count_before = len(self.amity.persons['fellows'].keys())

        self.assertEqual('Person: Jackson Nania already exists',
                         str(self.amity.add_person('Jackson Nania', 'FELLOW')))

        count_after = len(self.amity.persons['fellows'].keys())
        self.assertEqual(count_after, count_before,
                         msg='Records should be consistent')
        # test allocates when room available
        self.amity.create_room(['Narnia'], 'OFFICE')
        self.amity.add_person('Simam', 'FELLOW')
        self.assertTrue(self.amity.persons['fellows']['SIMAM'].office_space ==
                        'NARNIA', msg='Should allocate space')
        self.amity.create_room(['Mida'], 'LIVING')
        self.amity.add_person('Achach', 'FELLOW', 'Y')
        self.assertTrue('MIDA' in
                        self.amity.persons['fellows']['ACHACH'].living_space)
        # test rejects staff accommodation
        count_before = len(self.amity.persons['staff'])
        count_after = len(self.amity.persons['staff'])
        self.assertEqual('Staff cannot request for accommodation',
                         self.amity.add_person('Ali', 'STAFF', 'Y'))
        self.assertEqual(count_after, count_before, msg='No change in staff')


if __name__ == '__main__':
    unittest.main()
