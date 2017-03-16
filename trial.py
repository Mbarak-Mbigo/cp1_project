from app.amity import Amity

amity = Amity()
# amity.create_room("office", ['Mida', 'Krypton','Tsavo', 'Hogwarts', 'Valhalla'])
# amity.create_room("living", ['Go', 'PHP', 'Swift'])
amity.create_room('office', ['Bugatti', 'Range'])
amity.add_person('Rayyah Timamy', 'STAFF')
amity.print_unallocated()
amity.print_allocations()

amity.reallocate_person(amity.all_persons[0].id, "Bugatti")
amity.print_unallocated()
amity.print_allocations()