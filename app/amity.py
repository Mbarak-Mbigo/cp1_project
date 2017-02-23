# app/amity.py
# TODO integrate app with docopt
class Amity(object):
    def __init__(self, room_id=None, name = "Amity", location="Nairobi"):
        self.facility_id = room_id
        self.facility_name =name
        self.facility_location = location
        self.rooms = []  #confirm its the best way to implement composition list/dictionary
                        #a dictionary {room_name: room_object}
        self.persons = [] # counter check its the best way to implement aggregation list/dictionary
        
    def create_room(self, room_name, type=None):
        pass
        """"
        create_room --living_space "Pretoria"
        one name or many names
        Creates rooms in Amity <office | living_space>
        able to create many rooms at once (specify room name(s))
        """
    
    def add_person(self, person_name, person_type=None, wants_accommodation='N'):
        pass
        """"
        Add person to the system,
            create person
            add to system amity
        allocate the person to a random room
            if Staff allocate office space
            if Fellow and wants_accommodation is Yes
            allocate both office and living space (confirm procedure with TTL)
        """
    
    def allocate_room(self, person_id):
        pass
        """"
        allocate process should be random
        able to handle multiple allocations as well as
        one allocation
        What if person does not exist?
        what if person exists but is staff?
        what if person already allocated space?
        what if room to allocate if fully occupied?
        """
    
    def reallocate_room(self, person_id, new_room_name):
        pass
        """"
        reallocate the person with person_id provided to the
        new_room_name (unallocate, then reallocate
        what if person does not exist?
        What if person exists but is staff?
        What if room does not exist?
        what if room is fully occupied?
        """
    
    def load_people(self):
        pass
        """"
        Add people to rooms from a text file
        """
    
    def print_allocations(self, outfile=None):
        pass
        """"
        print a list of rooms and the people allocated into them
        if outfile provided output list to the file ( what if
        the file does not exist? create one or?
        """
    
    def print_unallocated(self, outfile=None):
        pass
        """"
        print a list of all unallocated people on the screen
        if outfile is provided, output the list to the file
        provided (what if the file does not exist? create one or?)
        """
    
    def print_room(self, room_name):
        pass
        """"
        print a list of all the people allocated in room_name
        """
    
    #added functionality
    def print_available_space(self):
        pass
        """"
        print all rooms and spaces available on each room (unallocated space)
        """