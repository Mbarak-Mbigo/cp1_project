# app/amity.py
# TODO integrate app with docopt


class Amity(object):
    rooms = []
    persons = []
        
    def create_room(self,type, rooms=[]):
        """"
        room type:String values: "Office"| "Living Space"
        Scenarios: Input not in specified options
            raise exception ValueError
        
        rooms type: String List values: Room names
        Scenarios: 
            Empty list
                raise Exception ValueError
            Non-empty but has one or more non-string data
                raise exception ValueError
            non-empty and data is string
                create room(s), update number of rooms
                return room created
        """
    
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
        person_id: id   values: list of ids in person
        Scenario:
            Id not in valid range
            Id in range
                Person unallocated
                    raise an exception
                Person allocated
                    Person Staff
                        reallocate living space
                            raise exception (type???)
                        reallocate office
                            space not available
                                raise exception/ print error msg???
                            space available
                                reallocate
                    Person Fellow
                        Reallocate living space
                            space not available
                                raise exception/ print error msg???
                            space available
                                reallocate
                                    do updates
                        Reallocate office space
                            Space not available
                                raise exception/ print error msg???
                            space available
                                reallocate
                                    do updates

            new_room_name: room values: names from rooms
            Scenario:
                Room name not among those in room pool
                    raise exception
                Room among those in pool
                    room fully occupied
                        raise exception
                    room not fully occupied
                        person staff room living space
                            raise exception

        """
        pass
    
    def load_people(self, filename):
        """"
        filename: txt file  values: person names and details
        Scenario:
            File does not exist
                raise exception file not exist
            File Exists
                file type not txt
                    raise exception
                file type txt
                    No data
                        Raise exception
                    Data exists
                            Unkown format
                                raise exception
                            data format okay
                                perform load operation

        """
        pass
    
    def print_allocations(self, outfile=None):
        """"
        print to the screen a list of rooms and the people allocated into them
        if outfile provided output list to the file  as well
        
        Scenario:
        No rooms or rooms available but no allocations yet
            raise exception
        Rooms available allocations okay
            outfile provided
                print to screen and file
            outfile not provided 
                print to screen

        """
        pass
    
    def print_unallocated(self, outfile=None):
        """"
        print a list of all unallocated people on the screen
        if outfile is provided, output the list to the file
        
        Scenario:
        No person
            responde accordingly
        People available
            No one unallocated
                handle accordingly
            Office
                fellows 
                staff
            living space
                fellows

        outfile provided
            output to file too.
        """

        pass
    
    def print_room(self, room_name):
        """"
        Given a room name, print all the people allocated to
        that room

        Scenarios:
        room not in pool
            raise exception
        room in pool
            no allocations
                handle accordingly
            allocations available
                display allocations
        """
        pass

    def save_state(self, database="default-db"):
        """"Persists all that in the application onto an
            SQLite database"""
        pass
        
    def load_state(self, database=None):
        """"Loads data from the provided database into the
        application for use
        
        Scenarios:
        db provided does not exist
            raise exception
        db exists
            no data
                raise exception
            data exists
                unkown format
                    raise exception
                known format
                    load data
                        unsuccessful
                            raise error
                        successful
                            load data
        """
        pass
    
    #added functionality
    def print_available_space(self):
        """
        print all rooms and spaces available on each room (unallocated space)
        Scenarios:

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

    def get_random_room(self, type=None):
        """ 
        Scenario: 
        No rooms
            raise exception
        Rooms available
            type: none
                consider all categories (office/living space)
            type: Office
                consider office category
            type: Living Space
        """
        pass
    
    def search_room(self, room_name, type=None):
        """
        search for room(s) in Amity
        if no input is provided, return the whole list of rooms
        Scenario:
        type: None
            consider searching all categories (office and living space)
        type: Office
            consider searching office category
        type: Living Space
            consider searching living space
        type: other
            raise exception

        room_name: 
            Not a string
                raise exception
            string
                not found
                    raise exception
                found
                    return room object
        """
        pass

    def search_person(self, person_name, type=None):
        """
        Seach for a person in Amity return None or person object
        Scenario:
        type: None
            consider person domain (all staff and fellow)
        type: Fellow
            consider fellow domain
        type: Staff
            consider staff domain
        type: other
            raise exception

        person_name
            not string
                raise exception
            string
                not found
                    raise exception
                found
                    return person object
        
        """
        pass


    