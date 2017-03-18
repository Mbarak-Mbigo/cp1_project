# tests/test_amity.py
# TODO add doc strings on tests, more descriptive names for tests
# TODO implement all test cases for amity
# imports
from Amity.app.amity import Amity
from person import Staff, Fellow
from room import office, LivingSpace

import unittest


class TestAmity(unittest.TestCase):
    # fixtures
    def setUp(self):
        self.amity = Amity()
        
    def tearDown(self):
        del self.amity
    
    # tests
    def test_raises_exception_on_input_not_type_string_list(self):
        """"Test raises an exception on all input types except string"""
        with self.assertRaises(ValueError) as error_info:
            self.amity.create_room("office", ["Runda", "Dar", 13])
        self.assertTrue("Input should be a list of strings" in str(error_info.exception))
            
    def test_creates_room(self):
        """"Test creates rooms of all types """
        self.amity.create_room("office", ["Mida","Mirema", "Ruai"])
        self.amity.create_room("Living", ["Swift", "Erlang"])
        self.assertEqual(len(self.amity.all_rooms), 5, msg="Should create rooms")
        self.assertTrue("Mida" in self.amity.search_rooms("office"))
        self.assertTrue("Swift" in self.amity.search_rooms("Living"))
        with self.assertRaises(ValueError) as error_info:
            self.amity.create_room("Another", ["Specialroom"])
        self.assertTrue("Invalid room type" in str(error_info.exception))

        
    
    def test_allocating_living_space_to_staff_raises_permissionerror(self):
        """" Test trying to allocate a staff Livings
            raises permission error error """
        with self.assertRaises(PermissionError) as error_info:
            self.amity.add_person("Maureen Nyakio", "Staff", "Y")
        self.assertTrue("Staffs are not allowed livingallocation" in str(error_info.exception))
    
    #
    def test_allocating_space_when_none_exists_raises_an_error(self):
        """"Test allocating space to people when no space exist
            raises an error"""
        fellow = Fellow("Maureen Wanja", "Fellow")
        with self.assertRaises(RuntimeError) as error_info:
            self.amity.allocate_room(fellow.id)
        self.assertTrue("Facility is full cannot allocate space" in error_info.exception)
    
    def test_reallocates_room_person(self):
        """"Test can reallocate a person from one room to another"""
        
        # staff
        self.assertEqual(len(self.amity.all_rooms),0 )
        self.amity.create_room("office", ["Mida"])
        self.assertEqual(len(self.amity.all_rooms), 1, msg="Should add office room")
        self.amity.add_person("Maureen Nyakio", "Staff")
        self.assertEqual(len(self.amity.persons), 1)
        # assert room occupants ==1
        self.assertEqual(len(self.amity.all_rooms[0].occupants), 1, msg="Number of occupants should increase")
        # assert room occupant is user created and allocated
        self.assertTrue(self.amity.all_rooms[0].occupants[0] == "Maureen Nyakio")

        self.amity.create_room("office", ["Terrace"])
        self.assertEqual(len(self.amity.all_rooms), 2, msg="Should add office room")
        person_to_relocate = self.amity.search_person('Maureen Nyakio')
        self.amity.reallocate_person(person_to_relocate.id, "Terrace")
        self.assertEqual(len(self.amity.all_rooms[0].occupants), 0, msg="Number of occupants should decrease")
        self.assertEqual(len(self.amity.all_rooms[1].occupants), 1, msg="Number of occupants should increase")

        # fellow and livingreallocation
        self.amity.create_room("Living", ["Swift", "Go"])
        self.assertEqual(len(self.amity.all_rooms), 4, msg="Should add livingrooms")
        self.amity.add_person("Oliver Tambo", "Fellow", "Y")
        self.assertEqual(len(self.amity.persons), 1, msg="Number of persons should increase")
        self.assertEqual(len(self.amity.all_rooms[3].occupants), 1, "Number of occupants should increase")

        self.amity.reallocate_person("fellow_id", "Go")
        self.assertEqual(len(self.amity.all_rooms[3].occupants), 0, "Number of occupants should decrease")
        self.assertEqual(len(self.amity.all_rooms[4].occupants), 1, "Number of occupants should increase")
        # Test reallocating office to livingRaises an Exception
        # Test reallocating Staff to livingRaises an Exception
        # Test reallocating a person not allocated yet raises an Error/Exception


        
    def test_loads_people_from_a_file(self):
        """"Test loads people from a file"""
        oldstate = len(self.amity.all_persons)
        self.amity.load_people("datafile.txt")
        self.assertGreater(len(self.amity.all_persons), oldstate, msg="Should have more people after loading")
    
    def test_displays_room_allocations_and_adds_content_to_file(self):
        """"Test displays room allocations and adds the data to a file when """
        f = open("allocations.txt", "w+")
        content = self.amity.print_allocations("allocations.txt")
        f.close()
        self.assertIn(content, self.amity.all_rooms, msg="Should add allocation data to file and print to screen")

    
    def test_prints_people_allocated_in_a_given_room(self):
        """"Given a room print all people allocated in that room"""
        self.amity.create_room("Mandiba")
        self.assertEqual(self.amity.all_rooms,1)
        staff = Staff( "Benjamin Mwashumbe")
        staff1 = Staff("Daudi Malisho")
        self.amity.allocate_room(staff.id)
        self.amity.allocate_room(staff1.id)
        self.assertIn("Benjamin Mwashumber",self.amity.all_rooms[0].occupants, msg="Should print room allocations data")

    def test_saves_data_into_a_database(self):
        """"Test saves data into a database"""
        conn = self.amity.save_state("amitydb")
        self.assertTrue(conn, msg="Should save data into a database")
        
    def test_loads_data_from_database_to_application(self):
        """"Test loads data from a database into the application
            """
        self.amity.load_state("amitydb")
        self.assertGreater(len(self.amity.all_rooms), 0, msg="Failed to load data from database")
    
        
     
if __name__ == '__main__':
    unittest.main()
