from state import *

b = Board()
p1 = Player(1)
p2 = Player(2)



p2.move(4,7,b)
p1.place_wall(Tile(4,7),b,"vertical")
p1.move(4,1,b)
p1.move(4,2,b)
p1.move(4,3,b)
p1.move(4,4,b)
p1.move(4,5,b)
p1.move(4,6,b)
p2.print_player()
p1.move(5,7,b)
#p1.move(4,8,b)

p1.print_player()
