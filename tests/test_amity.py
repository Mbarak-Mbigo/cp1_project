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
        self.assertTrue('Narnia already exists' in
                        str(self.amity.create_room(['Narnia'], 'OFFICE')))
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
        self.assertTrue('JACKSON NANIA' in self.amity.persons['fellows'].keys())
        self.amity.add_person('Rehema Tanya', 'STAFF')
        self.assertTrue('REHEMA TANYA' in self.amity.persons['staff'].keys())

        # Test rejects duplicate
        count_before = len(self.amity.persons['fellows'].keys())
        err_msg = self.amity.add_person('Jackson Nania', 'FELLOW')
        self.assertTrue('Person: Jackson Nania already exists' in repr(err_msg))
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
        err_msg = self.amity.add_person('Ali', 'STAFF', 'Y')
        count_after = len(self.amity.persons['staff'])
        self.assertTrue('Staff cannot request for accommodation' in str(err_msg))
        self.assertEqual(count_after, count_before, msg='No change in staff')

        # test reallocation
    def test_reallocate_person(self):
        """Test reallocates successfully."""
        self.amity.create_room(['Chanda'], 'OFFICE')
        self.amity.add_person('Ann', 'FELLOW')
        self.amity.create_room(['Mida'], 'OFFICE')
        self.amity.reallocate_person(self.amity.persons['fellows']['ANN'].id,
                                     'MIDA')
        self.assertTrue(self.amity.persons['fellows']['ANN'].office_space ==
                        'MIDA')

    """DB tests.
        createdb
        check db does not exist is true
        create db
        check db exists is true

        save state
        check drop if exists and create returns true
        check if records added is same as number of records in app

        load state tests
        a reversal of save state tests
    """
if __name__ == '__main__':
    unittest.main()
