class Player:

    def __init__(self, player_num):
        self.walls = 10

        if (player_num == 1):
            self.x = 4
            self.y = 0
        elif (player_num == 2):
            self.x = 4
            self.y = 8

    def legal_move(x,y):
        if (x<0 or x>8 or y<0 or y>8):
            return False
        if (board.players[2].x == x and board.players[2].y == y):
            return False
        #TODO: Check for pawn straight and L-shaped jumps
        return True


    def move(x,y, board):
        if legal_move(x,y):
            self.x = x
            self.y = y
        else:
            raise ("Illegal move")

    def legal_placement(tile):
        if (self.walls == 0):
            return False
        if (tile.x<0 or tile.x>=8 or tile.y<=0 or tile.y>8):
            return False
        # TODO: check if path to other side is completely blocked
        return True

    # place_wall(tile) places a wall where tile is the top_left tile
    def place_wall(tile, board, orientation):
        if legal_placemnt(tile):
            
            self.walls -= 1

            x = tile.x
            y = tile.y

            # Create remaining three tiles for wall object
            top_l = tile
            top_r = Tile(x+1, y)
            bot_l = Tile(x, y-1)
            bot_r = Tile(x-1, y-1)

            wall = Wall(top_l, top_r, bot_l, bot_r, orientation)
            board.walls.append(wall)
        else:
            raise ("Illegal wall placement")

    def print_player(self):
        print "Player's location: (%d, %d)\nWalls remaining: %d\n" % (self.x, self.y, self.walls)

class Tile:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print_tile(self):
        print "Tile location: (%d, %d)\n" % (self.x, self.y)

class Wall:

    def __init__(self, top_l, top_r, bot_l, bot_r, orientation):
        self.top_l = top_l
        self.top_r = top_r
        self.bot_l = bot_l
        self.bot_r = bot_r
        self.orientation = orientation

class Board:
    
    
    def __init__(self):
        self.players = [Player(1), Player(2)]
        self.walls = []
        self.tiles = [ [],[],[],[],[],[],[],[],[] ]
        
        for i in range(0,8):
            for j in range(0,8):
                self.tiles[i].append(Tile(i,j))

    def print_board(self):
        print self.tiles
        












        
