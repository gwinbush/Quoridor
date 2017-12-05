from Queue import *
import state
from sys import maxint

def aStarLength(start, end, state):
	path = aStar(start, end, state)
	return len(path)

def pathExists(start, end, state):
	path = aStar(start, end, state)
	if path == []:
		return False
	return True

def aStar(start, end, state):
	visited = set()
	frontier = list()
	frontier.append(start)
	cameFrom = {}
	
	gScore = {}
	for i in range(0,9):
		for j in range(0,9):
			gScore[(i,j)] = maxint
	gScore[start] = 0

	fScore = {}
	fScore = {}
	for i in range(0,9):
		for j in range(0,9):
			fScore[(i,j)] = maxint

	fScore[start] = heuristic(start, end)

	while len(frontier) != 0:
		current = smallest(frontier, fScore)
		if current == end:
			return make_path(cameFrom, current)
		
		frontier.remove(current)
		visited.add(current)

		children = get_successors(current)
		for child in children:
			if not (child in visited):
				if not blocked(child[0], child[1], current[0], current[1], state):
					frontier.append(child)

			tent_gScore = gScore[current] + 1
			if tent_gScore >= gScore[child]:
				continue

			cameFrom[child] = current
			gScore[child] = tent_gScore
			fScore[child] = gScore[child] + heuristic(child, end)
	return []

def make_path(cameFrom, current):
	tot_path = [current]
	while current in cameFrom.keys():
		current = cameFrom[current]
		tot_path.append(current)
	return tot_path

		
def smallest(frontier, fScore):
	smallest = frontier[0]
	for node in frontier:
		if fScore[node] < fScore[smallest]:
			smallest = node
	return smallest

def heuristic(start, end):
	return abs(start[1]-end[1])


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

def path(start, end, board):
	
	frontier = Queue()
	visited = set()
	frontier.put(start)
	visited.add(start)
	distance = {}
	distance[start] = 0
	while not frontier.empty():
		parent = frontier.get()
		if (parent == end):
			return distance[end]
		
		children = get_successors(parent)
		for child in children:
			if not (child in visited):
				if not blocked(child[0], child[1], parent[0], parent[1], board):
					frontier.put(child)
					distance[child] = distance[parent] + 1
					visited.add(child)
	
	return maxint

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
        """ Return True if move from (x1,y1) to (x2,y2) is blocked and False otherwise. """

        for wall in board.walls:
            if (wall.orientation == "horizontal"):
                if (y1 < y2):
                    if (wall.top_l.y == y1 and (wall.top_l.x == x1 or (wall.top_l.x + 1) == x1)):
                        return True
                if (y1 > y2):
                    if (wall.top_l.y == y2 and (wall.top_l.x == x1 or (wall.top_l.x + 1) == x1)):
                        return True
            if (wall.orientation == "vertical"):
                if (x1 < x2):
                    if (wall.top_l.x == x1 and (wall.top_l.y == y1 or (wall.top_l.y  + 1) == y1)):
                        return True
                if (x1 > x2):
                    if (wall.top_l.x == x2 and (wall.top_l.y == y2 or (wall.top_l.y + 1) == y2)):
                        return True
        return False
