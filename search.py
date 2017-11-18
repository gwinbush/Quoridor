from Queue import *
import state


def bfs(start, end, board):
	"""
    Breadth-first search function for tiles in game.

    Parameters
    ----------
    start : (int,int)
        starting location for search
    end : (int,int)
		ending location for search
	board : Board
		The game board that contains the start and end tiles for BFS 
    Returns
    -------
    bool
        True -- If a path exists from start to end. A path exists if the there is
        series of valid moves beginning at [start] and ending at [end]. A move
        is valid if it is not blocked by a wall and is a move to an adjacent
        tile or a valid jump 
        
        False -- Otherwise

    """
	frontier = Queue()
	visited = set()
	frontier.put(start)
	visited.add(start)
	while not frontier.empty():
		parent = frontier.get()
		if (parent == end):
			return True
		
		children = get_successors(parent)
		for child in children:
			if not (child in visited):
				if not blocked(child[0], child[1], parent[0], parent[1], board):
					frontier.put(child)
					visited.add(child)
	return False

def get_successors(parent):
	""" Return the tiles adjacent to [parent] """

	children = set()
	p0 = parent[0]
	p1 = parent[1]
	x1 = parent[0] - 1
	x2 = parent[0] + 1
	y1 = parent[1] - 1
	y2 = parent[1] + 1
	if (x1 >= 0):
		children.add((x1,p1))
	if (y1 >= 0):
		children.add((p0,y1))		
	if (x2 <= 8):
		children.add((x2,p1))		
	if (y2 <= 8):
		children.add((p0,y2))
	return children

def blocked(x1, y1, x2, y2, board):
	""" Return True if move from (x1,y1) to (x2,y2) is blocked and False otherwise """
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