# amity_refactor.py

# app/amity.py
# TODO integrate app with docopt
from random import choice

# local imports
from room import office, LivingSpace
from person import Staff, Fellow


class Amity(object):
    all_rooms = []
    all_persons = []
        
    def create_room(self,room_type, rooms=[]):
        """"
        room type:String values: "office"| "Living"
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
        try:
            if room_type not in ["office", "Living"]:
                raise ValueError("Invalid room type, it should be office or Living")
            elif not isinstance(rooms, list):
                raise TypeError("Provide a list of room name")
            elif not all(isinstance(x, str) for x in rooms):
                raise ValueError("Room should be string")
                
        except (ValueError,TypeError) as e:
            return e
        else:
            if room_type == "office":
                for room in rooms:
                    if len(self.search_rooms(room)) == 0:
                        self.all_rooms.append(office(room, room_type))
            else:
                for room in rooms:
                    if len(self.search_rooms(room)) == 0:
                        self.all_rooms.append(LivingSpace(room, room_type))

    
    def add_person(self, name, type, wants_accommodation='N'):
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
            allocate both office and Living
            return person added
            or Raise exception
        """
        try:
            person = None
            if not isinstance(name, str):
                raise ValueError("Person name can only be a string")
            elif type not in ["Staff", "Fellow"]:
                raise ValueError("Person type can only be Staff or Fellow")
            elif wants_accommodation not in ["Y", "N"]:
                raise ValueError("Wants accommodation can only be 'Y' or 'N' ")
            elif not isinstance(name, str):
                raise ValueError("Person name can only be a string")
            elif type == "Staff" and wants_accommodation == "Y":
                raise PermissionError("Staff cannot request for accommodation in Amity")
        except (ValueError, PermissionError) as e:
            print (e)
        else:
            if len(self.search_person(name)) == 0:
                if type == "Staff":
                    self.all_persons.append(Staff(name, type))
                    person = self.all_persons[-1]
                else:
                    self.all_persons.append(Fellow(name, type))
                    person = self.all_persons[-1]

                # allocate a person a room logic
                # Scenario
                # room = self.get_random_room()
                #  fellow: office|Living
                # staff: office
                self.allocate_room(person[0].id)
                
        finally:
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
                        reallocate Living
                            raise exception (type???)
                        reallocate office
                            space not available
                                raise exception/ print error msg???
                            space available
                                reallocate
                    Person Fellow
                        Reallocate Living
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
                        person staff room Living
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
            office
                fellows 
                staff
            Living
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
        What if person does not exist?
        what if person exists but is staff?
        what if person already allocated space?
        what if room to allocate if fully occupied?
        """
        try:
            if type(person_id) is not int:
                raise TypeError("Invalid person Id type")
        except TypeError as e:
            print (e)
        else:
            person = [person for person in self.all_persons if person.id == person_id]
            if isinstance(person, list) and len(person)==1:
                print("Yaaaaay! person found! id= %d" % person[0].id)
                # verified person is in the system
                if person[0].type == "Staff":
                    print("Person is staff allocate office space")
                else:
                    print("Person is Fellow")
            else:
                print("Oops no person found with id: %d" % person_id)
        finally:
            pass

    def get_random_room(self, type, current_room=None):
        """ 
        Scenario: 
        No rooms
            raise exception
        Rooms available
            type: none
                consider all categories (office/Living)
            type: office
                consider office category
            type: Living
            type: other
        """
        try:
            if type not in ["office", "Living"]:
                raise ValueError("Room type can only be office or Living")
            elif not isinstance(current_room, str) and current_room is not None:
                raise ValueError("Room name must be a string")
        except ValueError as e:
            print (e)
        else:
            # no rooms created yet
            if len(self.all_rooms)==0:
                return []
            else:
                room_pool = [room for room in self.all_rooms if room.type == type and room.name is not current_room]
                # no rooms to reallocate to (available room is the one already allocated to)
                if len(room_pool) == 0:
                     return []
                else:
                    return choice(room_pool)
        finally:
            pass
    
    def search_rooms(self, first_search_term=None ,second_search_term=None):
        """
        first_search-term = [None, office, Living, other]
        second_search_term = [None, office, Living, other]
        search for room in Amity
        Scenario:
        type: None
            consider searching all categories (office and Living)
        type: office or Living
            search all rooms
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

        rooms in system:
        No rooms
            return empty list
        rooms in system:
            search:
                found
                    return room object
                not found
                    return empty list
        """
        try:
            if  first_search_term not in [None, "office", "Living"] and not isinstance(first_search_term, str)\
            or second_search_term not in [None, "office", "Living"] and not isinstance(second_search_term, str):
                raise TypeError("Invalid Search Value(s)")
            elif first_search_term == None and second_search_term == None:
                raise ValueError("Search Values not provided")
        except (TypeError,ValueError) as e:
            print(e)
        else:
            # no rooms created yet
            if not isinstance(self.all_rooms, list):
                return []
            elif first_search_term == "office" and second_search_term== None:
                return [room for room in self.all_rooms if room.type == first_search_term]
            elif first_search_term == "Living" and second_search_term== None:
                return [room for room in self.all_rooms if room.type == first_search_term]
            elif isinstance(first_search_term, str) and second_search_term == None:
                return  [room for room in self.all_rooms if room.name == first_search_term]
            elif first_search_term in ["office", "Living"] and isinstance(second_search_term, str):
                return [room for room in self.all_rooms if room.type == first_search_term and room.name == second_search_term]
        
    def search_person(self, first_search_term, second_search_term=None):
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
        try:
            if second_search_term not in [None, "Fellow", "Staff"]:
                raise ValueError("No such person type")
            elif not isinstance(first_search_term, str):
                raise TypeError("Person names can only be of type string")
        except (TypeError, ValueError) as e:
            print(e)
        else:
            if not isinstance(self.all_persons, list):
                return []
            elif first_search_term in ["Fellow", "Staff"] and second_search_term == None:
                return [person for person in self.all_persons if person.type == first_search_term]
            elif isinstance(first_search_term, str) and second_search_term in ["Fellow", "Staff"] :
                return [person for person in self.all_persons if person_type == second_search_term and person.name == first_search_term]
            elif isinstance(first_search_term, str) and second_search_term == None:
                return [person for person in self.all_persons if person.name == first_search_term]


    





# trail.py code
# # # facility/app/trial.py

# # try:
# #     age = int(input("Please enter your age: "))
# # except Exception as err:
# #     # raise
# #     print("You entered incorrect age input: %s" % err)
# # else:
# #     print ("I see your age is: %s" % age)
# # finally:
# #     pass

# import logging

# logging.basicConfig(filename='myprogram.log', level=logging.ERROR)

# logging.error("The washing machine is leaking!")
# logging.critical("The house is on fire!")

# logging.warning("We are almost out of milk.")
# logging.info("It's sunny today.")
# logging.debug("I had eggs for breakfast")

# try:
#     age = int(input("How old are you? "))
# except Exception as e:
#     # raise
#     logging.exception(e)
# else:
#     pass
# finally:
#     pass

from amity import Amity

amity = Amity()
amity.create_room("Living",["Mombasa"])
# amity.create_room("office",["Mida"])
# print (len(amity.all_rooms))
# print (amity.all_rooms[0].rooms)
# print (amity.all_rooms)

print (amity.add_person("Arafat","Staff"))
print (amity.add_person("Aisha","Fellow"))
print (amity.add_person("Timina","Staff"))

print (len(amity.all_persons))
print (amity.all_persons[0].persons)
print (amity.all_persons[1].persons)
print("Found rooms")
print(amity.get_random_room("Living"))
amity.allocate_room(amity.all_persons[0].id)
