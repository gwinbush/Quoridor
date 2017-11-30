from state import *
import random

class Baseline(Player):
	def __init__(self, num):
		super(Baseline, self).__init__(num)

	def finalMove(self, state):
		moves = self.possibleMoves(state)
		walls = self.possibleWalls(state)
		choice = random.randint(0,len(moves))
		if choice == len(moves):
			wall = random.choice(walls)
			self.place_wall(state, wall)
		else:
			self.move(moves[choice].x, moves[choice].y, state)


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
		for i in range(8):
			for j in range(8):
				for k in ["horizontal", "vertical"]:
					top_l = Tile(i,j)
					top_r = Tile(i+1,j)
					bot_l = Tile(i,j+1)
					bot_r = Tile(i+1,j+1)
					wall = Wall(top_l, top_r, bot_l, bot_r, k)
					if self.legal_placement(state, wall):
						walls.append(wall)
		return walls



