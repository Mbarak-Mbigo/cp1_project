# app/amity.py
# TODO integrate app with docopt
from random import choice
import os

# local imports
from app.room import office, livingSpace
from app.person import Staff, Fellow


class Amity(object):
    accommodation = None
    all_rooms = []
    all_persons = []
        
    def create_room(self, room_type, rooms):
        """Create room(s).
        create_room <room_name>... - Creates rooms in Amity.
        Using this command I should be able to create as
        many rooms as possible by specifying multiple room
         names after the create_room command.
        Args:
            room_type: type of room (office|living).
            rooms: A list of room names (any string)
        Returns:
            Room(s) created.
        Raises:
            TypeError: if rooms not a list.
            ValueError: if rooms not strings
            ValueError: if room_type type not in (office| living).
        """
        try:
            if room_type not in ["office", "living"]:
                raise ValueError("Invalid room type, it should be office or living")
            elif not isinstance(rooms, list):
                raise TypeError("Provide a list of room name(s)")
            elif len(rooms)== 0 or not all(isinstance(x, str) for x in rooms):
                raise ValueError("Room names are supposed to be non-empty strings")
                
        except (ValueError,TypeError) as e:
            return e
        else:
            if room_type == "office":
                for room in rooms:
                    if len(self.search_rooms(room)) == 0:
                        self.all_rooms.append(office(room, room_type))
                return self.all_rooms[-1]
            else:
                for room in rooms:
                    if len(self.search_rooms(room)) == 0:
                        self.all_rooms.append(livingSpace(room, room_type))
                return self.all_rooms[-1]

    
    def add_person(self, name, type, wants_accommodation='N'):
        """Create a person, add to system, allocate to random room
        add_person <person_name> <FELLOW|STAFF> [wants_accommodation] - 
        Adds a person to the system and allocates the person to a random room. 
        wants_accommodation here is an optional argument which can be either Y or N. 
        The default value if it is not provided is N.
        Args:
            name: person name (string)
            type: person type (FELLOW | STAFF)
            wants_accommodation: ('Y' | 'N')
        Returns:
            Person created Object
        Raises:
            ValueError: if name not string
            ValueError: if type not in specified domain
            ValueError: if wants_accommodation not in specified domain
            PermissonError: if type is STAFF and wants_accommodation is 'Y'
        """
        try:
            person = None
            if not isinstance(name, str):
                raise ValueError("Person name can only be a string")
            elif type not in ["STAFF", "FELLOW"]:
                raise ValueError("Person type can only be Staff or Fellow")
            elif wants_accommodation not in ["Y", "N"]:
                raise ValueError("Wants accommodation can only be 'Y' or 'N' ")
            elif not isinstance(name, str):
                raise ValueError("Person name can only be a string")
            elif type == "STAFF" and wants_accommodation == "Y":
                raise PermissionError("Staff cannot request for accommodation in Amity")
        except (ValueError, PermissionError) as e:
            return e
        else:
            accommodation = wants_accommodation
            if len(self.search_person(name)) == 0:
                if type == "STAFF":
                    self.all_persons.append(Staff(name, type))
                    person = self.all_persons[-1]
                else:
                    self.all_persons.append(Fellow(name, type))
                    person = self.all_persons[-1]

                # allocate a person a room logic
                # Scenario
                # room = self.get_random_room()
                #  fellow: office|living
                # staff: office
                self.allocate_room(person.id, accommodation)
        finally:
            pass
    
    def reallocate_person(self, person_id, new_room_name):
        """Reallocate a person from one room to another
        reallocate_person <person_identifier> <new_room_name> - 
        Reallocate the person with person_identifier to new_room_name.
        
        Args: 
            person_id: (fellow | Staff)
            new_room_name: a valid room 

        Returns:
            Reallocated person

        Raises:
            ValueError: if person_id or new_room_name does not exist in System
            NotImplementedError: if unallocated person is reallocated
                                 if staff being reallocated to living
                                 if person being reallocated from one type to another
            SystemError: if no rooms available for rellocation

            ******handle for livingspace and office
        """
        try:
            current_room = None
            person = next((person for person in self.all_persons if person.id == person_id),None)
            reallocate_room = next((room for room in self.all_rooms if room.name == new_room_name),None)
            current_room = next((room_name for room in self.all_rooms if room.room_id == person.office_space),None)
            
            if person.type is "STAFF" and reallocate_room.type is "living":
                raise NotImplementedError("Staff cannot be reallocated to living")
            elif person.office_space is "None" and reallocate_room.type is "office":
                raise ValueError("Allocate office space first before reallocating")
            elif person.type is "FELLOW" and reallocate_room.type is "living":
                if person.livingspace is None:
                    raise ValueError("Allocate livingbefore reallocating")
                else:
                    current_room = next((room for room in self.all_rooms if room.room_id == person.livingspace),None)
            elif len(self.all_rooms) <= 1 or len(self.all_rooms) ==2 and len(self.search_rooms("office"))==1: 
                raise ValueError("No Space to reallocate")


        except (ValueError, NotImplementedError) as e:
            return e
        else:
            if reallocate_room.type is "office" and current_room.type is "office":
                current_room.occupants.remove(person.id)
                reallocate_room.occupants.append(person_id)
                person.office_space = reallocate_room.room_id
            elif reallocate_room.type is "living" and current_room is "living":
                current_room.occupants.remove(person_id)
                reallocate_room.occupants.append(person_id)
                person.livingspace = reallocate_room.room_id
        finally:
            pass
    
    def load_people(self, filename="data/load.txt"):
        """"
        Adds people to rooms from a txt file
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
        try:
            if not os.path.exists("data/load.txt"):
                raise FileNotFoundError("Loading file not found")
            elif os.stat("data/load.txt").st_size == 0:
                return "File is empty"

        except FileNotFoundError as e:
            return e
        else:
            with open("data/load.txt") as f:
                for line in f:
                    line = line.strip()
                    person_details = line.split(' ')
                    name = person_details[0] + ' ' + person_details[1]
                    person_type = person_details[2]
                    if person_details[-1] == "Y":
                        self.add_person(name, person_type, person_details[-1])
                    else:
                        self.add_person(name, person_type)
                print(len(self.all_persons))
                return "Loading operation successful"
        finally:
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
        try:
            occupied_rooms = None
            if len(self.all_rooms) == 0:
                raise ValueError("No rooms available")
            else:
                occupied_rooms = [room for room in self.all_rooms if len(room.occupants) > 0]
                if len(occupied_rooms) == 0:
                    raise ValueError("There are no allocations")

        except ValueError as e:
            return e
        else:
            print("ALLOCATIONS")
            for room in occupied_rooms:
                print("Room: %s" %room.name)
                print(room.occupants)
        finally:
            pass
    
    def print_unallocated(self, outfile=None):
        """"
        print a list of all unallocated people on the screen
        if outfile is provided, output the list to the file
        
        Scenario:
        No person
            respond accordingly
        People available
            No one unallocated
                handle accordingly
            office
                fellows 
                staff
            living
                fellows

        outfile provided
            output to file too.
        """
        try:
            unallocated = None
            if len(self.all_persons) == 0:
                raise ValueError("No people in the system")
            else:
                unallocated_office = [person for person in self.all_persons if person.office_space == None]
                staff = [person for person in self.all_persons if person.type == "STAFF"]
                unallocated_living = [person for person in self.all_persons if person.type == "FELLOW" and person.livingspace == None]
                print("Office Space: ")
                for person in unallocated_office:
                    print(person)
                print("\nLiving Space:")
                for person in unallocated_living:
                    print(person)
        except Exception as e:
            raise
        else:
            pass
        finally:
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
        try:
            room =next((room for room in self.all_rooms if room.name == room_name),None) 
            if room is None:
                raise ValueError("No room with name: %s" %room_name)
        except Exception as e:
            raise
        else:
            return room.occupants
        finally:
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
        args: None
        Returns: un allocated space
        Raise:
            ValueError: if no room space available

        """
        try:
            if len(self.all_rooms) == 0:
                raise ValueError("No room space available")
            
        except ValueError as e:
            return e
        else:
            office_space = [room for room in self.all_rooms if room.type == "office"]
            living_space = [room for room in self.all_rooms if room.type == "living"]
            print("AVAILABLE ROOMS:")
            for room in office_space:
               print(room)
            for room in living_space:
                print(room)
        finally:
            pass

    # Helper functions
    
    def allocate_room(self, person_id, accommodation):
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
            return e
        else:
            person = next((person for person in self.all_persons if person.id == person_id),None)
            if person is not None:
                # allocate office space
                office = self.get_random_room("office")
                if office is not None:
                    print("allocating office space")
                    office.occupants.append(person.name)
                    person.office_space = office.room_id

                if person.type == "FELLOW" and accommodation == 'Y':
                    print("allocating living space")
                    living_space = self.get_random_room("living")
                    if living_space is not None:
                        living_space.occupants.append(person.name)
                        person.livingspace = living_space.room_id
                
                return "Allocation Successful"

                
            else:
                print("Cannot assign space for person not in the system")
        finally:
            pass

    def get_random_room(self, type, current_room=None):
        """ 
        Scenario: 
        No rooms
            raise exception
        Rooms available
            type: none
                consider all categories (office/living)
            type: office
                consider office category
            type: living
            type: other
        """
        try:
            if type not in ["office", "living"]:
                raise ValueError("Room type can only be office or living")
            elif not isinstance(current_room, str) and current_room is not None:
                raise ValueError("Room name must be a string")
        except ValueError as e:
            print (e)
        else:
            # no rooms created yet
            if len(self.all_rooms)== 0:
                return None
            else:
                room_pool = [room for room in self.all_rooms if room.type == type and room.name is not current_room]
                # no rooms to reallocate to (available room is the one already allocated to)
                if len(room_pool) == 0:
                     return None
                else:
                    return choice(room_pool)
        finally:
            pass
    
    def search_rooms(self, first_search_term=None ,second_search_term=None):
        """
        first_search-term = [None, office, living, other]
        second_search_term = [None, office, living, other]
        search for room in Amity
        Scenario:
        type: None
            consider searching all categories (office and living)
        type: office or living
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
            if  first_search_term not in [None, "office", "living"] and not isinstance(first_search_term, str)\
            or second_search_term not in [None, "office", "living"] and not isinstance(second_search_term, str):
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
            elif first_search_term == "living" and second_search_term== None:
                return [room for room in self.all_rooms if room.type == first_search_term]
            elif isinstance(first_search_term, str) and second_search_term == None:
                return  [room for room in self.all_rooms if room.name == first_search_term]
            elif first_search_term in ["office", "living"] and isinstance(second_search_term, str):
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

    


    