from state import *
import search
import random
import copy 
from sys import maxint

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
			if minMovePath < minPath:
				minPath = minMovePath
				minMove = m

		min_diff = minPath - minOppPath

		min_wall = None
		if self.walls != 0:
			walls = self.possibleWalls(state)
			for w in walls:
				new_state = copy.deepcopy(state)
				new_state.walls.append(w)

				minWinPath = minPathLen(self.x, self.y, win_row, new_state)
				minOppPath = minPathLen(opp.x, opp.y, opp_row, new_state)
				diff = minWinPath - minOppPath
				if diff < min_diff:
					min_diff = diff
					min_wall = w

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

#Static Methods

def minPathLen(x, y, win_row, state):
	minPath = maxint
	for end in win_row:
		path_len = search.path((x, y), end, state)
		if  path_len< minPath:
			minPath = path_len
	return minPath





















