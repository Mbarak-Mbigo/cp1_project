"""Amity test suite.

tests/test.py

Process:
    Write a failing unit test
    Make the unit test pass
    Refactor
"""
# imports
import unittest
from unittest.mock import patch
import os

# local imports
from app.amity import Amity
from app.room import Room, Office, Living
from app.person import Person, Staff, Fellow


class AmityTests(unittest.TestCase):
    """Test Suite for Amity."""

    # fixtures
    def setUp(self):
        """Create necessary objects."""
        self.amity = Amity()

    def tearDown(self):
        """Reset necessary objects."""
        self.amity.rooms['offices'] = dict()
        self.amity.rooms['livingspaces'] = dict()
        self.amity.persons['staff'] = dict()
        self.amity.persons['fellows'] = dict()

    def test_person_functionality(self):
        """Test person functionality."""
        with self.assertRaises(TypeError):
            Person('Rudish Salim')
        staff = Staff('Amina Buhari', 1654)
        self.assertEqual('STAFF (id:1654 name:AMINA BUHARI office:None)',
                         repr(staff))

        fellow = Fellow('Imran', 4334)
        self.assertEqual(
            'FELLOW (id:4334 name:IMRAN office:None living:None '
            'accommodation:N', repr(fellow))

    # def test_room_functionality(self):
    #     """Test room functionality."""
    #     with self.assertRaises(TypeError):
    #         Room("Mida")
    #     office = Office('Ramire', 1001, ['samuel', 'ali', 'sam', 'Idi'])

    def test_creates_room(self):
        """Test rooms are created successfully."""
        # captures invalid input
        # Room type
        msg = self.amity.create_room(["Mida"], "Other_type")
        self.assertNotIn("Mida", self.amity.rooms['offices'].keys() and
                         self.amity.rooms['livingspaces'].keys())
        self.assertEqual('Invalid room type: Other_type', str(msg))
        # Room name not string
        msg = self.amity.create_room(["Mambrui", 334])
        self.assertTrue(334 not in self.amity.rooms['offices'].keys())
        self.assertEqual('Invalid room name type', str(msg))
        # Can create one room
        msg = self.amity.create_room(['Narnia'], 'OFFICE')
        self.assertTrue('NARNIA' in self.amity.rooms['offices'].keys())
        self.assertEqual('Success', msg)
        # Does not allow to create room(s) already existing
        self.assertEqual("Can't recreate existing rooms",
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
        # test only accepts string names
        self.assertEqual('Invalid type', str(self.amity.add_person(34343,
                                                                   'FELLOW')))
        # test does not accept types other than STAFF and FELLOW
        msg = self.amity.add_person('Samuel Bomu', 'other_type')
        self.assertEqual('Invalid person role', str(msg))
        # test adds succesfully
        self.amity.add_person('Jackson Nania', 'FELLOW')
        self.assertTrue('JACKSON NANIA' in
                        self.amity.persons['fellows'].keys())

        self.amity.add_person('Rehema Tanya', 'STAFF')
        self.assertTrue('REHEMA TANYA' in self.amity.persons['staff'].keys())

    #     # Test rejects duplicate
        count_before = len(self.amity.persons['fellows'].keys())

        self.assertEqual('Double entry not allowed',
                         str(self.amity.add_person('Jackson Nania', 'FELLOW')))

        count_after = len(self.amity.persons['fellows'].keys())
        self.assertEqual(count_after, count_before,
                         msg='Records should be consistent')
        # test allocates when room available
        self.amity.create_room(['Hudaa'], 'OFFICE')
        self.amity.add_person('Simam', 'FELLOW')
        self.assertTrue(self.amity.persons['fellows']['SIMAM'].office_space)
        self.amity.create_room(['Mida'], 'LIVING')
        self.amity.add_person('Achach', 'FELLOW', 'Y')
        self.assertTrue('MIDA' in
                        self.amity.persons['fellows']['ACHACH'].living_space)
        # test rejects staff accommodation
        count_before = len(self.amity.persons['staff'])
        count_after = len(self.amity.persons['staff'])
        self.assertEqual('Invalid request',
                         self.amity.add_person('Ali', 'STAFF', 'Y'))
        self.assertEqual(count_after, count_before, msg='No change in staff')
        self.assertEqual(str(self.amity.add_person('Amir', 'fellow', 'Z')),
                         'Invalid accommoation type')

    def test_reallocates(self):
        """Test reallocates people from one room to another."""
        # Does not reallocate to non existent room
        self.assertEqual(len(self.amity._get_all_rooms()), 0)
        self.amity.add_person('Salma', 'STAFF')
        self.amity.add_person('Naidy', 'fellow')
        msg = self.amity.reallocate_person(
            self.amity.persons['staff']['SALMA'].id, 'Zen')
        self.assertEqual('No rooms', str(msg))
        self.amity.create_room(['Subra'], 'office')
        msg = self.amity.reallocate_person(
            self.amity.persons['staff']['SALMA'].id, 'Zen')
        self.assertEqual('No such room', str(msg))
        # Handles nonexistent person
        self.assertEqual(str(self.amity.reallocate_person(324, 'Subra')),
                         'No such person')
        # Does not reallocate unallocated
        self.assertEqual(self.amity.reallocate_person(
            self.amity.persons['staff']['SALMA'].id, 'Subra'),
            'unallocated staff')
        self.assertEqual(self.amity.reallocate_person(
            self.amity.persons['fellows']['NAIDY'].id, 'Subra'),
            'unallocated fellow office')
        # Does not reallocate staff to living space
        self.amity.allocate_room('Salma')
        self.amity.create_room(['Mida'], 'living')
        self.assertEqual(self.amity.reallocate_person(
            self.amity.persons['staff']['SALMA'].id, 'Mida'),
            'Invalid operation')
        # Does not reallocate to the same office
        self.assertEqual(self.amity.reallocate_person(
            self.amity.persons['staff']['SALMA'].id, 'Subra'),
            'Same office')
        # Reallocates office space
        self.amity.create_room(['Nadra'], 'office')
        self.assertEqual(self.amity.reallocate_person(
            self.amity.persons['staff']['SALMA'].id, 'Nadra'),
            'Success')
        self.assertTrue(self.amity.persons['staff']['SALMA'].office_space ==
                        'NADRA')
        # Reallocates living space
        self.amity.add_person('Samuel', 'fellow', 'Y')
        self.amity.create_room(['React'], 'living')
        # Does not reallocate to the same living room
        msg = self.amity.reallocate_person(
            self.amity.persons['fellows']['SAMUEL'].id, 'Mida')
        self.assertFalse(msg == 'Success')
        msg = self.amity.reallocate_person(
            self.amity.persons['fellows']['SAMUEL'].id, 'React')
        self.assertTrue(msg == 'Success')
        self.amity.allocate_room('Naidy')
        self.assertEqual(self.amity.reallocate_person(
            self.amity.persons['fellows']['NAIDY'].id, 'React'),
            'unallocated fellow living')

    def test_unallocated_persons(self):
        """Test allocates unallocated and prints unallocated."""
        # Does not allocate if not people in the system
        self.assertTrue(str(self.amity.allocate_room()) == 'No person yet')
        self.assertEqual(str(self.amity.print_unallocated()), 'Empty')
        self.amity.add_person('Amina', 'fellow', 'Y')
        self.amity.add_person('Ridhaa', 'fellow')
        self.amity.add_person('Faizi', 'staff')
        self.amity.add_person('Aladin', 'staff')
        self.amity.create_room(['Tida'], 'office')
        self.amity.create_room(['Runda'], 'living')
        self.amity.allocate_room()
        self.assertEqual(self.amity.print_unallocated(), 'No unallocated')

    def test_print_room(self):
        """Test print room allocation details."""
        # Handles nonexistent room
        self.assertTrue(str(self.amity.print_room('Linter')) ==
                        'No room with name: Linter')
        # Reports contextual feedback
        self.amity.create_room(['Linter'], 'office')
        self.assertEqual(self.amity.print_room('Linter'), 'No allocations')
        self.amity.add_person('Dennis Mwangi', 'staff')
        self.amity.add_person('Evans Nduati', 'fellow')
        self.assertEqual(self.amity.print_room('Linter'), 'Success')

    def test_print_allocations(self):
        """Test allocations are printed and handled accordingly."""
        # Reports contextual feedback
        self.assertTrue(str(self.amity.print_allocations()) == 'No rooms')
        self.amity.create_room(['Oval'], 'office')
        self.amity.create_room(['Square'], 'living')
        self.assertTrue(str(self.amity.print_allocations()) ==
                        'No allocations')
        self.amity.add_person('Rukia Adam', 'staff')
        self.amity.add_person('Eugene Said', 'fellow', 'Y')
        self.assertEqual(str(self.amity.print_allocations()), 'print success')
        self.assertEqual(str(self.amity.print_allocations('allocations.txt')),
                         'Success')

    @patch('app.amity.os')
    def test_load_people(self, mock_os):
        """Test load_people."""
        mock_os.path.exists.return_value = False
        self.amity.load_people('mock_data.txt')
        self.assertFalse(mock_os.stat.called, 'Invalid path')

        mock_os.path.exists.return_value = True
        mock_os.stat('data/mock_data.txt').st_size = 0
        self.assertTrue(self.amity.load_people('mock_data.txt') ==
                        'Empty file')

    def test_load_people_with_data(self):
        """Test data loaded successfully."""
        self.assertTrue(self.amity.load_people('load.txt') == 'success')

    def test_print_unallocated(self):
        """Test unallocated people are printed and saved to file."""
        self.amity.add_person('Cynthia Simon', 'staff')
        self.amity.add_person('Rudisha Said', 'staff')
        self.amity.add_person('Maureen Muriithi', 'fellow')
        self.amity.add_person('Ali Daudi', 'fellow', 'Y')
        self.assertTrue(self.amity.print_unallocated() == 'unallocated exists')
        self.assertEqual(self.amity.print_unallocated('unallocated.txt'),
                         'success write')

    def test_print_available_space(self):
        """Test printing available space functionality."""
        self.assertTrue(str(self.amity.print_available_space()),
                        'No space available')
        self.amity.create_room(['Nina', 'Twina'], 'office')
        self.amity.create_room(['Swift', 'Shina'], 'living')
        self.assertTrue(str(self.amity.print_available_space()),
                        'success')

    def test_save_state(self):
        """Test states are saved successfully."""
        self.amity.create_room(['Swift', 'Jaudi'], 'office')
        self.amity.create_room(['Zimer', 'Roysa'], 'living')
        self.amity.add_person('Ali', 'staff')
        self.amity.add_person('Omar', 'staff')
        self.amity.add_person('Subira', 'staff')
        self.amity.add_person('Ridhaa', 'fellow')
        self.amity.add_person('Salma', 'fellow', 'Y')
        self.assertTrue(self.amity.save_state('testdata.db') ==
                        'save successful')
        self.assertTrue(os.path.exists('databases/testdata.db'), 'True')

    def test_load_state(self):
        """Test loads data from database."""
        self.assertEqual(str(self.amity.load_state('nonexistent.db')),
                         'database does not exist')
        # Handles nonexistent databases well
        self.assertEqual(str(self.amity.load_state('testda.db')),
                         'database does not exist')
        self.assertEqual(self.amity.load_state('testdata.db'), 'Operation successful')


if __name__ == '__main__':
    unittest.main()
