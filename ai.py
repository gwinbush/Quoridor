from state import *
import search
import random
import copy 
from sys import maxint
minint = -maxint -1

class Baseline(Player):
	def __init__(self, num):
		super(Baseline, self).__init__(num)
		self.wall_options = []
		for i in range(8):
			for j in range(8):
				for k in ["horizontal", "vertical"]:
					top_l = Tile(i,j)
					top_r = Tile(i+1,j)
					bot_l = Tile(i,j+1)
					bot_r = Tile(i+1,j+1)
					wall = Wall(top_l, top_r, bot_l, bot_r, k)
					self.wall_options.append(wall)

	def finalMove(self, state):
		moves = self.possibleMoves(state)
		walls = self.possibleWalls(state)
		choice = random.randint(0,len(moves))
		if choice == len(moves) and self.walls !=0:
				try:
					wall = random.choice(self.wall_options)
					self.place_wall(state, wall)
				except:
					self.finalMove(state)
		
		elif self.walls == 0:
			choice = random.randint(0,len(moves)-1)
			self.move(moves[choice].x, moves[choice].y, state)

		else:
			self.move(moves[choice].x, moves[choice].y, state)

		# print search.path((self.x, self.y), (4,0), state)


	def possibleMoves(self, state):
		moves = []
		moves.append(Tile(self.x, self.y-1))
		moves.append(Tile(self.x, self.y+1))
		moves.append(Tile(self.x+1, self.y))
		moves.append(Tile(self.x-1, self.y))

		result = []
		for m in moves:
			if self.legal_move(m.x, m.y, state):
				result.append(m)
		return result

	def possibleWalls(self, state):
		walls = []
		for wall in self.wall_options:
			if True:#self.legal_placement(state, wall):
				walls.append(wall)
		return walls


class Roger(Player):
	def __init__(self, num):
		super(Roger, self).__init__(num)
		self.wall_options = []
		for i in range(8):
			for j in range(8):
				for k in ["horizontal", "vertical"]:
					top_l = Tile(i,j)
					top_r = Tile(i+1,j)
					bot_l = Tile(i,j+1)
					bot_r = Tile(i+1,j+1)
					wall = Wall(top_l, top_r, bot_l, bot_r, k)
					self.wall_options.append(wall)
		if self.player_num == 1:
			self.win_row = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0)]
			self.opp_row = [(0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8)]
		else:
			self.opp_row = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0)]
			self.win_row = [(0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8)]


	def finalMove(self, state):
		min_diff = maxint

		opp_row = self.opp_row
		opp = state.players[0]
		minOppPath = minPathLen(opp.x, opp.y, opp_row, state)

		minPath = maxint
		minMove = None
		moves = self.possibleMoves(state)

		win_row = self.win_row
		for m in moves:
			minMovePath = minPathLen(m.x, m.y, win_row, state)
			rand = random.randint(0,7)
			if (minMovePath < minPath):
				if self.walls == []:
					minPath = minMovePath
					minMove = m
				elif (rand < 7):
					minPath = minMovePath
					minMove = m
		min_diff = minPath - minOppPath

		min_wall = None
		if self.walls != 0:
			walls = self.possibleWalls(state)
			for w in walls:
				state.walls = state.walls + [w]
				minWinPath = minPathLen(self.x, self.y, win_row, state)
				minOppPath = minPathLen(opp.x, opp.y, opp_row, state)
				diff = minWinPath - minOppPath
				rand = random.randint(0,30==20)
				if (diff < min_diff) and (rand < 19):
					min_diff = diff
					min_wall = w
				state.walls = state.walls[:-1]

		if min_wall == None:
			self.move(minMove.x, minMove.y, state)
		else:
			self.place_wall(state, min_wall)
			

	def possibleMoves(self, state):
		moves = []
		moves.append(Tile(self.x, self.y-1))
		moves.append(Tile(self.x, self.y+1))
		moves.append(Tile(self.x+1, self.y))
		moves.append(Tile(self.x-1, self.y))
		
		result = []
		for m in moves:
			if self.legal_move(m.x, m.y, state):
				result.append(m)
		return result


	def possibleWalls(self, state):
		walls = []
		for wall in self.wall_options:
			if self.legal_placement(state, wall):
				walls.append(wall)
		return walls

class Mrinal(Player):
	def __init__(self, num):
		super(Mrinal, self).__init__(num)
		self.wall_options = []
		for i in range(8):
			for j in range(8):
				for k in ["horizontal", "vertical"]:
					top_l = Tile(i,j)
					top_r = Tile(i+1,j)
					bot_l = Tile(i,j+1)
					bot_r = Tile(i+1,j+1)
					wall = Wall(top_l, top_r, bot_l, bot_r, k)
					self.wall_options.append(wall)
		if self.player_num == 1:
			self.win_row = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0)]
			self.opp_row = [(0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8)]
			self.opp_num = 0
		else:
			self.opp_row = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0)]
			self.win_row = [(0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8)]
			self.opp_num = 1

	def finalMove(self, state):
		moves = {}
		possible_walls = possibleWalls(self.player_num, state)
		possible_moves = possibleMoves(self.player_num, state)

		for m in possible_moves:
			node = Node(self.player_num, state, "move", None, m.x, m.y)
			moves[node] = self.miniMax(node, 0, True)
		for w in possible_walls:
			node = Node(self.player_num, state, "wall", w)
			moves[node] = self.miniMax(node, 0, True)
		
		move = min(moves, key=moves.get)

		if move.move_type == "move":
			self.move(move.x, move.y, state)
		else:
			move.wall.print_wall()
			self.place_wall(state, move.wall)
			

	def miniMax(self, node, depth, maximizingPlayer):
		if depth == 0 or self.winningMove(node):
			return heuristic(self, node, node.state)

		if maximizingPlayer:
			bestValue = minint
			bestMove = None
			children = node.children()
			for child in children:
				v = self.miniMax(child, depth-1, False)
				bestValue = max(bestValue, v)
			return bestValue

		else:
			bestValue = maxint
			children = node.children()
			for child in children:
				v = miniMax(child, depth-1, True)
				bestValue = min(bestValue, v)
			return bestValue


	def winningMove(self, node):
		if node.move_type == "move":
			if (node.x, node.y) in self.win_row:
				return True
		return False


def heuristic(player, node, st):
	opp_row = player.opp_row
	if player.player_num == 1:
		opp = st.players[0]
	else:
		opp = st.players[1];

	if node.move_type == "move":
		minMovePath = minPathLen(node.x, node.y, player.win_row, st)
		minOppPath = minPathLen(opp.x, opp.y, opp_row, st)
		return minOppPath - minMovePath
	else:
		st.walls = st.walls + [node.wall]
		minWinPath = minPathLen(player.x, player.y, player.win_row, st)
		minOppPath = minPathLen(opp.x, opp.y, opp_row, st)
		return minOppPath - minWinPath
		
#Static Methods

def minPathLen(x, y, win_row, state):
	minPath = maxint
	for end in win_row:
		path_len = search.path((x, y), end, state)
		if  path_len< minPath:
			minPath = path_len
	return minPath

def possibleMoves(player_num, state):
	moves = []
	moves.append(Tile(state.players[player_num].x, state.players[player_num].y-1))
	moves.append(Tile(state.players[player_num].x, state.players[player_num].y+1))
	moves.append(Tile(state.players[player_num].x+1, state.players[player_num].y))
	moves.append(Tile(state.players[player_num].x-1, state.players[player_num].y))
	
	result = []
	for m in moves:
		if state.players[player_num].legal_move(m.x, m.y, state):
			result.append(m)
	return result


def possibleWalls(player_num, state):
	walls = []
	for wall in state.players[player_num].wall_options:
		if state.players[player_num].legal_placement(state, wall):
			walls.append(wall)
	return walls

class Node():
	def __init__(self, player_num, state, move_type, wall=None, x=None, y=None):
		self.move_type = move_type
		self.wall = wall
		self.x = x
		self.y = y
		self.player_num = player_num
		self.state = state
		if player_num == 0:
			self.opp_num = 1
		else:
			self.opp_num = 0

	def children(self):
		children = []
		new_state = copy.deepcopy(self.state)
		if self.move_type == "move":
			new_state.players[self.opp_num].x = self.x
			new_state.players[self.opp_num].y = self.y
		else:
			new_state.walls.append(self.wall)

		possible_moves = possibleMoves(self.opp_num, new_state)
		possible_walls = possibleWalls(self.opp_num, new_state)
		for m in possible_moves:
			node = Node(player_num, new_state, "move", None, m.x, m.y)
			children.append(node)
		for w in possible_walls:
			children.append(Node(player_num, new_state, "wall", w))
		return children
