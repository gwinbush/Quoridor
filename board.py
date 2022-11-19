from state import *
from sys import argv
import Tkinter
import math
import time
import threading
import random
import time

TILE_SIZE = 50
PLAYER_SIZE = int(0.8 * TILE_SIZE)
TILE_PADDING = 10
BORDER = 10
NUM_ROWS = 9
NUM_COLUMNS = NUM_ROWS
CONTROL_WIDTH = 200
COLORS = {
    "bg": "#FFFFFF",
    "tile": "#d0d0d0",
    "wall": "#008000",
    "wall-error": "#CC1111",
    "panel": "#333333",
    "button": "#555555",
    "text": "#000000",
    "players": ["#00F", "#ff0000"],
    "players-shadows": ["#9999ff", "#ffbdbd"],
}
PLAYERS = ["Blue", "Red"]


class Board:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.width = 0
        self.height = 0
        self.players = [None, None]
        self.tiles = []
        self.walls = {}
        self.move = None
        self.player_shadow = None
        self.wall_shadow = None
        self.turn = 0
        self.state = None
        self.photo = None
        self.ai_count = "0"
        self.wall_elements = [None, None]
        self.current_element = None
        for _ in range(NUM_COLUMNS):
            self.tiles.append(range(NUM_ROWS))

    def newGame(self, ai_count):
        if self.root:
            self.root.destroy()

        self.root = Tkinter.Tk()
        self.root.title("Quoridor")

        self.root.bind("<Escape>", lambda e: self.handleQuit())
        self.root.bind("w", lambda e: self.setMove("placeWall"))
        self.root.bind("m", lambda e: self.setMove("movePawn"))
        self.root.bind("<Motion>", lambda e: self.handleMotion(e.x, e.y))
        self.root.bind("<Button-1>", lambda e: self.handleClick(e.x, e.y))

        self.height = (NUM_ROWS * TILE_SIZE) + (NUM_ROWS * TILE_PADDING) + (2 * BORDER)
        self.width = self.height + CONTROL_WIDTH
        self.canvas = Tkinter.Canvas(
            self.root, width=self.width, height=self.height, background=COLORS["bg"]
        )
        self.canvas.pack()
        self.drawTiles()
        self.generateWalls()

        self.state = State(ai_count)
        self.ai_count = ai_count
        self.turn = self.state.current
        self.drawPlayers()
        self.drawInstructions()
        self.drawWallCount()
        self.drawCurrentPlayerTurn()

        self.root.mainloop()

    def drawInstructions(self):
        if int(self.ai_count) == 0:
            x = self.width - CONTROL_WIDTH / 2 - BORDER
            y = 3 * BORDER
            i = "Player 1 is the Blue Player and Player 2 is the Red Player!"
            self.canvas.create_text(
                (x, y), text=i, justify="center", width=CONTROL_WIDTH
            )

        elif int(self.ai_count) == 1:
            x = self.width - CONTROL_WIDTH / 2 - BORDER
            y = 3 * BORDER
            i = "You are the Blue Player and your opponent is the Red Player!"
            self.canvas.create_text(
                (x, y), text=i, justify="center", width=CONTROL_WIDTH
            )

        elif int(self.ai_count) == 2:
            x = self.width - CONTROL_WIDTH / 2 - BORDER
            y = 3 * BORDER
            i = "Let's see which bot will emerge victorious!"
            self.canvas.create_text(
                (x, y), text=i, justify="center", width=CONTROL_WIDTH
            )

        x = self.width - CONTROL_WIDTH / 2 - BORDER / 2
        y = 12 * BORDER
        i = "Instructions: \n Press 'm' to move your pawn to an appropriate square with a click. Press 'w' to place a wall with a click"
        self.canvas.create_text((x, y), text=i, justify="center", width=CONTROL_WIDTH)

        x = self.width - CONTROL_WIDTH / 2 - BORDER / 2
        y = self.height - 125
        self.photo = Tkinter.PhotoImage(file="quoridor.gif")
        self.photo.subsample(2, 2)
        self.canvas.create_image((x, y), image=self.photo)

    def drawWallCount(self):
        y = self.height / 2.75
        x = self.width - CONTROL_WIDTH / 2 - BORDER
        for p in self.state.players:
            output = ""
            output += PLAYERS[p.player_num] + " has " + str(p.walls) + " walls left"
            if self.wall_elements[p.player_num] == None:
                self.wall_elements[p.player_num] = self.canvas.create_text(
                    (x, y),
                    text=output,
                    justify="center",
                    width=CONTROL_WIDTH,
                    font=("Arial", 14, "bold"),
                )
            else:
                self.canvas.itemconfigure(self.wall_elements[p.player_num], text=output)
            y += 2 * BORDER

    def drawCurrentPlayerTurn(self):
        y = self.height / 1.8
        x = self.width - CONTROL_WIDTH / 2 - BORDER
        output = "It is " + PLAYERS[self.turn] + "'s Turn"
        if self.current_element == None:
            self.current_element = self.canvas.create_text(
                (x, y),
                text=output,
                justify="center",
                width=CONTROL_WIDTH,
                font=("Arial", 14, "bold"),
            )
        else:
            self.canvas.itemconfigure(self.current_element, text=output)

    def drawTiles(self):
        for j in range(NUM_ROWS):
            for i in range(NUM_COLUMNS):
                x = BORDER + TILE_PADDING / 2 + i * (TILE_SIZE + TILE_PADDING)
                y = BORDER + TILE_PADDING / 2 + j * (TILE_SIZE + TILE_PADDING)
                tile = self.canvas.create_rectangle(
                    x, y, x + TILE_SIZE, y + TILE_SIZE, fill=COLORS["tile"]
                )
                self.tiles[j][i] = tile

    def generateWalls(self):
        walls = []
        for j in range(0, NUM_ROWS - 1):
            for i in range(0, NUM_COLUMNS - 1):
                for k in [0, 1]:
                    if k == 0:
                        wall_string = str(j) + str(i) + "H"
                    else:
                        wall_string = str(j) + str(i) + "V"
                    x1, y1, x2, y2 = wallStrToCoords(wall_string)
                    wall = self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill="", outline=""
                    )
                    self.walls[wall_string] = wall

    def drawPlayers(self, shadow=False):
        for k in range(len(PLAYERS)):
            player = self.state.players[k]
            row = player.x
            column = player.y
            self.drawPlayer(row, column, k, player, shadow)

    def drawPlayer(self, row, column, num, player, shadow):
        x, y = gridToCoords(row, column)
        if x == None or y == None:
            return
        if not shadow and self.players[num]:
            self.canvas.delete(self.players[num])
            self.players[num] = None
        elif shadow and self.player_shadow:
            self.canvas.delete(self.player_shadow)
        color = COLORS["players"][num]
        if shadow:
            color = COLORS["players-shadows"][num]
        radius = PLAYER_SIZE / 2
        pawn = self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius, fill=color, outline=""
        )
        if not shadow:
            self.players[num] = pawn
        else:
            self.player_shadow = pawn

    def drawWalls(self, legal=False):
        for wall in self.state.walls:
            wall_string = wallStateToStr(wall)
            self.showWall(wall_string)
        if self.wall_shadow and self.move == "placeWall":
            self.showWall(self.wall_shadow, legal)

    def hideWall(self, wall_string):
        if wall_string in self.walls:
            self.canvas.itemconfigure(self.walls[wall_string], fill="")

    def showWall(self, wall_string, legal=True):
        if not legal:
            color = COLORS["wall-error"]
        else:
            color = COLORS["wall"]
        if wall_string in self.walls:
            w = self.walls[wall_string]
            self.canvas.itemconfigure(w, fill=color)

    def setMove(self, move):
        self.move = move
        self.refresh()

    def handleQuit(self):
        self.root.destroy()

    def handleMotion(self, x, y):
        if self.ai_count == "2" or (self.turn == 1 and self.ai_count == "1"):
            return

        self.clearWallShadow()
        i, j = coordsToGrid(x, y)
        if i == None or j == None:
            return
        if self.move == "movePawn":
            if self.state.players[self.turn].legal_move(i, j, self.state):
                self.drawPlayer(i, j, self.turn, self.state.players[self.turn], True)
            elif self.player_shadow != None:
                self.canvas.delete(self.player_shadow)
                self.player_shadow == None

        elif self.move == "placeWall":
            wall_string = coordsToWallStr(i, j, x, y)
            self.wall_shadow = wall_string
            legal = self.state.players[self.turn].legal_placement(
                self.state, wallStrToState(wall_string)
            )
            self.drawWalls(legal)

    def handleClick(self, x, y):
        if self.ai_count == "2":
            while (
                not self.state.players[0].winning_position
                and not self.state.players[1].winning_position
            ):
                self.state.players[self.turn].finalMove(self.state)
                self.nextTurn()
                self.refresh()
                time.sleep(0.1)

        else:
            i, j = coordsToGrid(x, y)
            if i == None or j == None:
                return

            if self.move == "movePawn":
                if self.state.players[self.turn].legal_move(i, j, self.state):
                    self.state.players[self.turn].move(i, j, self.state)
                    self.nextTurn()
                    self.refresh()

            if self.move == "placeWall":
                wall_string = coordsToWallStr(i, j, x, y)
                if self.state.players[self.turn].legal_placement(
                    self.state, wallStrToState(wall_string)
                ):
                    self.wall_shadow = None
                    self.state.players[self.turn].place_wall(
                        self.state, wallStrToState(wall_string)
                    )
                    self.nextTurn()
                    self.refresh()

            if self.handleWinner():
                return

            if self.turn == 1 and self.ai_count == "1":
                self.state.players[self.turn].finalMove(self.state)
                self.nextTurn()
                self.refresh()
                time.sleep(0.1)

    def handleWinner(self):
        winner = False
        for p in self.state.players:
            if p.winning_position:
                x = self.width - CONTROL_WIDTH / 2 - BORDER
                y = self.height / 2
                i = "Player " + PLAYERS[p.player_num] + " is the WINNER!"
                self.canvas.create_text(
                    (x, y),
                    text=i,
                    justify="center",
                    width=CONTROL_WIDTH,
                    font=("Arial", 14, "bold"),
                )
                winner = True
                break
        if winner:
            self.root.unbind("<Motion>")
            self.root.unbind("<Button-1>")
        return winner

    def refresh(self):
        self.clearShadow()
        self.clearWallShadow()
        self.drawWalls()
        self.drawWallCount()
        self.drawCurrentPlayerTurn()
        self.drawPlayers()
        self.root.update()
        self.handleWinner()

    def nextTurn(self):
        self.state.nextTurn()
        self.turn = self.state.current

    def clearShadow(self):
        if self.player_shadow != None:
            self.canvas.delete(self.player_shadow)
            self.player_shadow = None

    def clearWallShadow(self):
        if self.wall_shadow != None:
            self.hideWall(self.wall_shadow)
            self.wall_shadow = None


# Static Methods

# Returns center coordinate of tile(i,j)
def gridToCoords(i, j):
    if (0 <= i <= 8) and (0 <= j <= 8):
        x = BORDER + TILE_PADDING / 2 + (i) * (TILE_SIZE + TILE_PADDING)
        y = BORDER + TILE_PADDING / 2 + (j) * (TILE_SIZE + TILE_PADDING)
        return (x + (TILE_SIZE / 2)), (y + (TILE_SIZE / 2))
    else:
        return None, None


# Given mouse cooridinates x,y, returns grid position
def coordsToGrid(x, y):
    x -= BORDER
    y -= BORDER

    i = int(math.floor(float(x) / (TILE_SIZE + TILE_PADDING)))
    j = int(math.floor(float(y) / (TILE_SIZE + TILE_PADDING)))

    if (0 <= i <= 8) and (0 <= j <= 8):
        return i, j
    else:
        return None, None


# returns the top left and bottom right wall coords
def wallStrToCoords(wall_string):
    if len(wall_string) == 3:
        x = int(wall_string[0])
        y = int(wall_string[1])
        orientation = wall_string[2]
        cx, cy = gridToCoords(x, y)
        if orientation == "H":
            x1 = cx - TILE_SIZE / 2
            y1 = cy + TILE_SIZE / 2 + TILE_PADDING
            x2 = x1 + 2 * TILE_SIZE + TILE_PADDING
            y2 = y1 - TILE_PADDING
        else:
            x1 = cx + TILE_SIZE / 2
            y1 = cy + 3 * (TILE_SIZE / 2) + TILE_PADDING
            x2 = x1 + TILE_PADDING
            y2 = cy - TILE_SIZE / 2
        return x1, y1, x2, y2


# Given grid position i,j and mouse position x,y, returns correct wall_string
def coordsToWallStr(i, j, x, y):
    cx, cy = gridToCoords(i, j)
    dx = (2**0.5) * (x - cx)
    dy = (2**0.5) * (y - cy)
    orient = (dx - dy) * (dx + dy)
    if orient >= 0:
        orientation = "V"
    else:
        orientation = "H"
    if dx < 0 and i > 0:
        i -= 1
    if dy < 0 and j > 0:
        j -= 1
    return str(i) + str(j) + orientation


def wallStrToState(wall_string):
    orientation = "horizontal"
    if wall_string[2] == "V":
        orientation = "vertical"
    i = int(wall_string[0])
    j = int(wall_string[1])
    top_l = Tile(i, j)
    top_r = Tile(i + 1, j)
    bot_l = Tile(i, j + 1)
    bot_r = Tile(i + 1, j + 1)
    return Wall(top_l, top_r, bot_l, bot_r, orientation)


def wallStateToStr(wall):
    wall_string = ""
    wall_string += str(wall.top_l.x) + str(wall.top_l.y)
    o = wall.orientation
    if o == "horizontal":
        wall_string += "H"
    else:
        wall_string += "V"

    return wall_string


if __name__ == "__main__":
    board = Board()
    if len(argv) == 2:
        if argv[1] == "1":
            board.newGame("1")
        elif argv[1] == "2":
            board.newGame("2")
    else:
        board.newGame("0")
