"""Amity test suite.

tests/test.py

Process:
    Write a failing unit test
    Make the unit test pass
    Refactor
"""
# imports
import unittest

# local imports
from app.amity import Amity
from app.room import Room, Office, Living


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
        self.assertTrue('Narnia' not in self.amity.rooms['offices'].keys())
        self.amity.create_room(['Narnia'], 'OFFICE')
        self.assertTrue('Narnia' in self.amity.rooms['offices'].keys())
        # Does not allow to create room(s) already existing
        err_msg = self.amity.create_room(['Narnia'], 'OFFICE')
        self.assertTrue('Narnia already exists' in err_msg)
        # Can create many rooms
        num_of_rooms = (len(self.amity.rooms['livingspaces'].keys()))
        self.amity.create_room(['Tsavo', 'Zimmer'], 'LIVING')
        num_of_rooms_after = (len(self.amity.rooms['livingspaces'].keys()))
        self.assertGreater(num_of_rooms_after, num_of_rooms,
                           msg='Rooms should increase')
        self.assertEqual(num_of_rooms + 2, num_of_rooms_after,
                         msg='Rooms added should be equal to rooms created')

        # test room number increases
        # test creates living rooms, one and multiple
        # test crates office rooms, one and multiple
        pass

if __name__ == '__main__':
    unittest.main()
