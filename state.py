from search import *

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

    def move(self, x, y, board):
    	""" Try to move pawn to (x,y). Update the board if successful. Raise exception otherwise. """

        if self.legal_move(x, y, board):
            self.x = x
            self.y = y
            if (self.player_num == 1):
            	board.players[0] = self
            else:
            	board.players[1] = self
        else:
            raise ("Illegal move")
            
    def place_wall(self, tile, board, orientation):
    	"""place_wall(tile, board, orientation) places a wall where tile is the top_left tile """
        x = tile.x
        y = tile.y
        # Create remaining three tiles for wall object
        top_l = tile
        top_r = Tile(x+1, y)
        bot_l = Tile(x, y-1)
        bot_r = Tile(x-1, y-1)
        wall = Wall(top_l, top_r, bot_l, bot_r, orientation)

        if self.legal_placement(tile, board, wall):
            self.walls -= 1
            board.walls.append(wall)
        else:
            raise ("Illegal wall placement")
            
    def legal_move(self, x, y, board):
    	""" Return True if move to (x,y) is a legal move and False otherwise. """

        # Location is on the board
        if (x<0 or x>8 or y<0 or y>8):
            return False
        # Move is not to the same spot
        if (self.x == x and self.y == y):
        	return False
        #Check for pawn straight jumps
        if (not self.legal_jump(x,y,board) and (abs(self.y-y) > 1 or abs(self.x - x) > 1 or (abs(self.y-y) == 1 and abs(self.x - x) == 1))):
        	return False
        # Location is not occupied by the other player
        if self.occupied(x,y,board):
        	return False
        # Move is not blocked by a wall
        if self.blocked(self.x, self.y, x, y, board):
        	return False
        return True

    def occupied(self,x,y,b):
    	""" Return true if the tile (x,y) has a pawn on it and false otherwise. """

    	if (self.player_num == 1 and b.players[1].x == x and b.players[1].y == y):
            return True
        if (self.player_num == 2 and b.players[0].x == x and b.players[0].y == y):
            return True
        return False

    def legal_jump(self,x,y,b):
    	""" Return true if jump to (x,y) is legal and False otherwise. """

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
    	""" Return True if move from (x1,y1) to (x2,y2) is blocked and False otherwise. """

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
    	""" Return true if (x1,y1) and (x2,y2) are adjacent and False otherwise. """

    	if ((abs(x1-x2) == 1 and abs(y1-y2) == 0) or (abs(y1-y2) == 1 and abs(x1-x2) == 0)):
    		return True
    	return False

    def legal_placement(self, tile, board, wall):
    	""" Return True if it is legal to place [wall] at location [tile] and False otherwise.
    		[tile] is the upper left tile touching the wall. """

        # Player has enough walls
        if (self.walls == 0):
        	return False
        # Plecement is on the board
        if (tile.x<0 or tile.x>8 or tile.y<0 or tile.y>8):
            return False
        # Plecement does not intersect with another wall
        for w in board.walls:
        	if w.orientation == "horizontal" and wall.orientation == "horizontal":
        		if w.top_l.y == wall.top_l.y and ((w.top_l.x == wall.top_l.x) or (w.top_l.x-1 == wall.top_l.x) or (w.top_l.x+1 == wall.top_l.x)):
        			return False
        	if w.orientation == "vertical" and wall.orientation == "vertical":
        		if w.top_l.x == wall.top_l.x and ((w.top_l.y == wall.top_l.y) or (w.top_l.y-1 == wall.top_l.y) or (w.top_l.y+1 == wall.top_l.y)):
        			return False
        	if (w.top_l.x == wall.top_l.x and w.top_l.y == wall.top_l.y):
        		return False
        # Placement does not completely block either player from reaching winning tile
        if not self.path_exists(board, wall):
        	return False
        
        return True
    
    def path_exists(self, b, w):
    	""" Return True if both players have a path to their winning tiles and False otherwise. """

        new_b = b
        new_b.walls.append(w)
        p1_path = False
        p2_path = False
        win_row1 = [(0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8)]
        win_row2 = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0)]

        for tile in win_row1:
            if bfs((b.players[0].x,b.players[0].y), tile, b):
                p1_path = True
        for tile in win_row2:
            if bfs((b.players[1].x,b.players[1].y), tile, b):
                p2_path = True

        return (p1_path and p2_path)

    def print_player(self):
    	""" Display information about the player. """
        print "Player's location: (%d, %d)\nWalls remaining: %d\n" % (self.x, self.y, self.walls)

class Tile:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print_tile(self):
    	""" Display information about the tile. """
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
    	""" Display information about the board """
        print self.tiles
