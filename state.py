class Player:

    def __init__(self, player_num):
        self.walls = 10
        self.player_num = player_num

        if (player_num == 1):
            self.x = 4
            self.y = 0
        elif (player_num == 2):
            self.x = 4
            self.y = 8

    def legal_move(self, x, y, board):
        # Location is on the board
        if (x<0 or x>8 or y<0 or y>8):
            raise ("not on board")
        # Move is not to the same spot
        if (self.x == x and self.y == y):
        	raise ("same tile as current tile")
        #Check for pawn straight jumps
        if (not self.legal_jump(x,y,board) and (abs(self.y-y) > 1 or abs(self.x - x) > 1 or (abs(self.y-y) == 1 and abs(self.x - x) == 1))):
        	raise ("illegal jump!")
        # Location is not occupied by the other player
        if self.occupied(x,y,board):
        	raise ("Tile is occupied")
        # Move is not blocked by a wall
        if self.blocked(self.x, self.y, x, y, board):
        	raise ("blocked by wall")
        return True

    def occupied(self,x,y,b):
    	if (self.player_num == 1 and b.players[1].x == x and b.players[1].y == y):
            return True
        if (self.player_num == 2 and b.players[0].x == x and b.players[0].y == y):
            return True
        return False

    def legal_jump(self,x,y,b):    		
    	if self.player_num == 1:
    		opp_num = 2
    	else:
    		opp_num = 1

    	oppx = b.players[opp_num-1].x
    	oppy = b.players[opp_num-1].y
    	if (self.adjacent(self.x,self.y,oppx,oppy) and self.adjacent(oppx,oppy,x,y) and (not self.blocked(self.x,self.y,oppx,oppy,b)) and (not self.blocked(oppx,oppy,x,y,b))):
    		return True
    	return False

    def blocked(self, x1, y1, x2, y2, board):
    	for wall in board.walls:
    		if (wall.orientation == "horizontal"):
    			if (y1 < y2):
    				if (wall.top_l.y == y2 and (wall.top_l.x == x2 or (wall.top_l.x + 1) == x2)):
    					return True
    			if (y1 > y2):
    				if (wall.top_l.y == y1 and (wall.top_l.x == x1 or (wall.top_l.x + 1) == x1)):
    					return True
    		if (wall.orientation == "vertical"):
    			if (x1 < x2):
    				if (wall.top_l.x == x1 and (wall.top_l.y == y1 or (wall.top_l.y - 1) == y1)):
    					return True
    			if (x1 > x2):
    				if (wall.top_l.x == x2 and (wall.top_l.y == y2 or (wall.top_l.y - 1) == y2)):
    					return True
    	return False

    def adjacent(self,x1,y1,x2,y2):
    	if ((abs(x1-x2) == 1 and abs(y1-y2) == 0) or (abs(y1-y2) == 1 and abs(x1-x2) == 0)):
    		return True
    	return False

    def move(self, x, y, board):
        if self.legal_move(x, y, board):
            self.x = x
            self.y = y
            if (self.player_num == 1):
            	board.players[0] = self
            else:
            	board.players[1] = self
        else:
            raise ("Illegal move")

    def legal_placement(self, tile):
        if (self.walls == 0):
            return False
        if (tile.x<0 or tile.x>=8 or tile.y<=0 or tile.y>8):
            return False
        # TODO: check if path to other side is completely blocked
        return True

    # place_wall(tile, board, orientation) places a wall where tile is the top_left tile
    def place_wall(self, tile, board, orientation):
        if self.legal_placement(tile):
            
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
        












        
