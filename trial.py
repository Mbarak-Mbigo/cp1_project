from app.amity import Amity

amity = Amity()
# amity.create_room("office", ['Mida', 'Krypton','Tsavo', 'Hogwarts', 'Valhalla'])
# amity.create_room("living", ['Go', 'PHP', 'Swift'])
amity.load_people()
amity.print_unallocated('data/unallocated.txt')
amity.print_allocations("data/allocations.txt")