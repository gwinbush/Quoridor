from state import *
import search
import random
import copy
from sys import maxint

minint = -maxint - 1

# AI interface class
class AI(Player):
    def __init__(self, num):
        super(AI, self).__init__(num)
        if self.player_num == 1:
            self.win_row = [
                (0, 0),
                (1, 0),
                (2, 0),
                (3, 0),
                (4, 0),
                (5, 0),
                (6, 0),
                (7, 0),
                (8, 0),
            ]
            self.opp_row = [
                (0, 8),
                (1, 8),
                (2, 8),
                (3, 8),
                (4, 8),
                (5, 8),
                (6, 8),
                (7, 8),
                (8, 8),
            ]
            self.opp = 0
        else:
            self.opp_row = [
                (0, 0),
                (1, 0),
                (2, 0),
                (3, 0),
                (4, 0),
                (5, 0),
                (6, 0),
                (7, 0),
                (8, 0),
            ]
            self.win_row = [
                (0, 8),
                (1, 8),
                (2, 8),
                (3, 8),
                (4, 8),
                (5, 8),
                (6, 8),
                (7, 8),
                (8, 8),
            ]
            self.opp = 1


# Baseline AI finds all possible and randomly selects one
# We give it a higher probability of moving the pawn rather than placing a wall
class Baseline(AI):
    def __init__(self, num):
        super(Baseline, self).__init__(num)

    def finalMove(self, state):
        moves = self.possibleMoves(state)
        walls = self.possibleWalls(state)
        choice = random.randint(0, len(moves))
        if choice == len(moves) and self.walls != 0:
            try:
                wall = random.choice(self.wall_options)
                self.place_wall(state, wall)
            except:
                self.finalMove(state)

        elif self.walls == 0:
            choice = random.randint(0, len(moves) - 1)
            self.move(moves[choice].x, moves[choice].y, state)

        else:
            self.move(moves[choice].x, moves[choice].y, state)


class Heuristic(AI):
    def __init__(self, num):
        super(Heuristic, self).__init__(num)

    def finalMove(self, state):
        opp = state.players[self.opp]

        minOppPath = minPathLen(opp.x, opp.y, self.opp_row, state)
        minMovePath = minPathLen(self.x, self.y, self.win_row, state)
        # print str(minOppPath) + ' , ' + str(minMovePath)

        min_diff = maxint
        minPath = maxint
        minMove = None
        moves = self.possibleMoves(state)

        for m in moves:
            minMovePath = minPathLen(m.x, m.y, self.win_row, state)
            rand = random.randint(0, 7)
            if minMovePath < minPath:
                if self.walls == []:
                    minPath = minMovePath
                    minMove = m
                elif rand < 7:
                    minPath = minMovePath
                    minMove = m
        min_diff = minPath - minOppPath

        min_wall = None
        if self.walls != 0:
            walls = self.possibleWalls(state)
            for w in walls:
                state.walls = state.walls + [w]
                minWinPath = minPathLen(self.x, self.y, self.win_row, state)
                minOppPath = minPathLen(opp.x, opp.y, self.opp_row, state)
                diff = minWinPath - minOppPath
                rand = random.randint(1, 20)
                if (diff < min_diff) and (rand < 19):
                    min_diff = diff
                    min_wall = w
                state.walls = state.walls[:-1]

        if min_wall == None and minMove == None:
            self.finalMove(state)
        elif min_wall == None:
            self.move(minMove.x, minMove.y, state)
        else:
            self.place_wall(state, min_wall)

        minOppPath = minPathLen(opp.x, opp.y, self.opp_row, state)
        minMovePath = minPathLen(self.x, self.y, self.win_row, state)
        # print str(minOppPath) + ' , ' + str(minMovePath)


class Minimax(AI):
    def __init__(self, num):
        super(Minimax, self).__init__(num)

    def finalMove(self, state):
        moves = {}
        possible_walls = self.possibleWalls(state)
        possible_moves = self.possibleMoves(state)

        for m in possible_moves:
            node = Node(self.player_num, state, "move", None, m.x, m.y)
            # moves[node] = self.miniMax(node, 0, True)
            moves[node] = self.alphabeta(node, 0, minint, maxint, True)
        for w in possible_walls:
            node = Node(self.player_num, state, "wall", w)
            # moves[node] = self.miniMax(node, 0, True)
            moves[node] = self.alphabeta(node, 0, minint, maxint, True)

        move = max(moves, key=moves.get)

        if move.move_type == "move":
            self.move(move.moveX, move.moveY, state)
        else:
            self.place_wall(state, move.wall)

    def miniMax(self, node, depth, maximizingPlayer):
        if depth == 0 or self.winningMove(node):
            return self.heuristic(node, node.state)

        if maximizingPlayer:
            bestValue = minint
            bestMove = None
            children = node.children(maximizingPlayer)
            for child in children:
                v = self.miniMax(child, depth - 1, False)
                bestValue = max(bestValue, v)
            return bestValue

        else:
            bestValue = maxint
            children = node.children(maximizingPlayer)
            for child in children:
                v = miniMax(child, depth - 1, True)
                bestValue = min(bestValue, v)
            return bestValue

    def alphabeta(self, node, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.winningMove(node):
            return self.heuristic(node, node.state)

        if maximizingPlayer:
            bestValue = minint
            bestMove = None
            children = node.children(maximizingPlayer)
            for child in children:
                v = self.alphabeta(child, depth - 1, alpha, beta, False)
                bestValue = max(bestValue, v)
                alpha = max(alpha, bestValue)
                if beta <= alpha:
                    break
            return bestValue

        else:
            bestValue = maxint
            children = node.children(maximizingPlayer)
            for child in children:
                v = alphabeta(child, depth - 1, alpha, beta, True)
                bestValue = min(bestValue, v)
                if beta <= alpha:
                    break
            return bestValue

    def winningMove(self, node):
        if node.move_type == "move":
            if (node.moveX, node.moveY) in self.win_row:
                return True
        return False

    def heuristic(self, node, state):
        opp = state.players[self.opp]
        if node.move_type == "move":
            minMovePath = minPathLen(node.moveX, node.moveY, self.win_row, state)
            minOppPath = minPathLen(opp.x, opp.y, self.opp_row, state)
            return minOppPath - minMovePath
        else:
            state.walls = state.walls + [node.wall]
            minWinPath = minPathLen(self.x, self.y, self.win_row, state)
            minOppPath = minPathLen(opp.x, opp.y, self.opp_row, state)
            state.walls = state.walls[:-1]
            return minOppPath - minWinPath


class Node:
    # player in state makes move_type with wall or (moveX,moveY)
    def __init__(self, player_num, state, move_type, wall=None, moveX=None, moveY=None):
        self.move_type = move_type
        self.wall = wall
        self.moveX = moveX
        self.moveY = moveY
        self.player_num = player_num
        new_state = copy.deepcopy(state)
        if self.move_type == "move":
            new_state.players[self.player_num].x = self.moveX
            new_state.players[self.player_num].y = self.moveY
        else:
            new_state.players[self.player_num].place_wall(new_state, self.wall)

        self.state = new_state
        self.opp_num = new_state.players[self.player_num].opp

    def children(self, maximizingPlayer):
        children = []
        opponent_possible_moves = self.state.players[self.opp_num].possibleMoves(
            self.state, True
        )
        opponent_possible_walls = self.state.players[self.player_num].possibleWalls(
            self.state, True
        )
        for m in opponent_possible_moves:
            node = Node(self.opp_num, self.state, "move", None, m.x, m.y)
            children.append(node)
        for w in opponent_possible_walls:
            children.append(Node(self.opp_num, self.state, "wall", w))
        return children


# Static Methods
def minPathLen(x, y, win_row, state):
    minPath = maxint
    for end in win_row:
        path_len = search.path((x, y), end, state)
        if path_len < minPath:
            minPath = path_len
    return minPath
