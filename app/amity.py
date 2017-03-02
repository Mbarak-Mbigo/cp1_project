# app/amity.py
# TODO integrate app with docopt


class Amity(object):
    rooms = []
    persons = []
        
    def create_room(self,type, rooms=[]):
        """"
        room type:String values: "Office"| "Living Space"
        Scenarios: What if type not string, string but not among options
            raise exception ValueError
        
        rooms type: String List values: Room names
        Scenarios: 
            Empty list
                raise Exception ValueError
            Non-empty but has one or more non-string data
                raise exception ValueError
            non-empty and data is string
                create room(s), update number of rooms
        """
        pass
    
    def add_person(self,type, name, wants_accommodation='N'):
        """"
        type: String values: "Staff" | "Fellow"
        Scenario: Input not in specified options
            raise exception ValueError

        name: String values: person name
        Scenario: Input not string
            raise exception ValueError

        wants_accommodation: String Character values: "N" | "Y"
        Scenarios: Input not in specified options
            raise exception ValueError

        create person (add to amity: r/ship=> Aggregation)and 
        allocate them to a random room 
            {consume get_random_room to get random room}

        Add person to the system,
            create person
            add to system amity
        allocate the person to a random room
            if Staff allocate office space
            if Fellow and wants_accommodation is Yes
            allocate both office and living space
            return person added
            or Raise exception
        """
        pass
    
    def reallocate_person(self, person_id, new_room_name):
        """"
        reallocate the person with person_id provided to the
        new_room_name (unallocate, then reallocate
        what if person does not exist?
        What if person is staff?
        What if person is fellow?
            office space
            living space
        What if room does not exist?
        what if room is fully occupied?
        """
        pass
    
    def load_people(self, filename):
        """"
        Add people to rooms from a text file
        File exists
        File does not exist
        File is empty
        File has correct content
        """
        pass
    
    def print_allocations(self, outfile=None):
        """"
        print a list of rooms and the people allocated into them
        if outfile provided output list to the file ( what if
        the file does not exist? create one or?
        """
        pass
    
    def print_unallocated(self, outfile=None):
        """"
        print a list of all unallocated people on the screen
        if outfile is provided, output the list to the file
        provided (what if the file does not exist? create one or?)
        all staff with office attribute None
        all fellows with office none, and livingspace N
        """
        pass
    
    def print_room(self, room_name):
        """"
        Given a room name, print all the people allocated to
        that room
        """
        pass

    def save_state(self, database=None):
        """"Persists all that in the application onto an
            SQLite database"""
        pass
        
    def load_state(self, database=None):
        """"Loads data from the provided database into the
        application for use"""
        pass
    
    #added functionality
    def print_available_space(self):
        """
        print all rooms and spaces available on each room (unallocated space)
        """
        pass
        
    
        
    # Helper functions
    
    def allocate_room(self, person_id):
        """"
        allocate process should be random
        able to handle multiple allocations as well as
        one allocation
        What if person does not exist?
        what if person exists but is staff?
        what if person already allocated space?
        what if room to allocate if fully occupied?
        """
        pass

    def get_random_room(self):
        """ 
        Scenario: 
            No rooms: No room has been created or 
            All available rooms are fully occupied
        Using a random function,
         Pools of rooms
            Not fully occuppied
                Office
                Living Space
            return room object or None
        """
        pass
    
    def search_rooms(self, type=None, room_name=[]):
        """
        search for room(s) in Amity
        if no input is provided, return the whole list of rooms
        """
        pass

    def search_person(self, type=None, person_name=None):
        """Seach for a person in Amity return None or person object"""
        pass


    