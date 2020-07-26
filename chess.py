import pygame
from math import ceil
from random import random, shuffle

# assigns color values

black = (0, 0, 0)
white = (255, 255, 255)
forest = (50, 205, 50)
red = (212, 0, 0)
sky = (123, 211, 247)
player_colors = (False, (204, 110, 255), (250, 162, 67))

# draws an empty chessboard

def drawBlank():
    screen.fill(black)
    for i in range(4):
        for j in range(4):
            for k in range(2):
                pygame.draw.rect(
                    screen, white, (i * 200 + k * 100, j * 200 + k * 100, 100, 100))

# draws all game pieces in their current positions

def renderPieces():
    for piece in pieces:
        if piece.alive:
            placeInSquare(piece.icon, piece.x, piece.y)

# converts a given x or y coordinate to the x or y value of the cell it is in

def roundCell(coordinate):
    coordinate /= 100
    coordinate = ceil(coordinate)
    return coordinate

# shades a given cell (x and y are between 1 and 8, starting at (1, 1) in the top left)


def shadeCell(color, x, y):
    pygame.draw.rect(screen, color, ((x - 1) * 100, (y - 1) * 100, 100, 100))

# draws squares at the top right of pieces to identify their team

def highlight():
    for i in range(8):
        for j in range(8):
            if getSide(i + 1, j + 1) == 1:
                pygame.draw.rect(screen, player_colors[1], (i * 100 + 90, j * 100, 10, 10))
            elif getSide(i + 1, j + 1) == -1:
                pygame.draw.rect(screen, player_colors[-1], (i * 100 + 90, j * 100, 10, 10))

# shortcut for drawing the board and pieces

def initialize():
    drawBlank()
    highlight()
    renderPieces()

# draws a piece at a given cell

def placeInSquare(piece, x, y):
    screen.blit(piece, ((x - 1) * 100 + 18, (y - 1) * 100 + 18))

# returns the side of the piece at a certain location; returns 0 if the cell is empty

def getSide(x, y):
    for piece in pieces:
        if piece.x == x and piece.y == y and piece.alive:
            return piece.side
    return 0

# returns the maximum of two numbers

def max(a, b):
    if a > b:
        return a
    return b

# returns the minimum of two numbers

def min(a, b):
    if a < b:
        return a
    return b

class Piece:
    def __init__(self, x, y, side, icon):
        self.icon = icon
        self.side = side
        self.alive = True
        self.x = x
        self.y = y
        self.moved = False


class Pawn(Piece):
    def validMove(self, x, y):
        if self.moved == False and self.x == x and self.y == y + (2 * self.side) and getSide(self.x, self.y - self.side) == 0 and getSide(x, y) == 0:
            return True
        elif self.x == x and self.y == y + self.side and getSide(x, y) == 0:
            return True
        elif abs(x - self.x) == 1 and self.y == y + self.side and getSide(x, y) != getSide(self.x, self.y) and getSide(x, y) != 0:
            return True
        return False


class Knight(Piece):
    def validMove(self, x, y):
        if abs(x - self.x) == 2 and abs(y - self.y) == 1:
            return True
        elif abs(x - self.x) == 1 and abs(y - self.y) == 2:
            return True
        return False


class Rook(Piece):
    def validMove(self, x, y):
        if self.x == x:
            minimum = min(self.y, y)
            maximum = max(self.y, y)
            for i in range(maximum - minimum - 1):
                if getSide(x, minimum + 1 + i) != 0:
                    return False
            return True
        elif self.y == y:
            minimum = min(self.x, x)
            maximum = max(self.x, x)
            for i in range(maximum - minimum - 1):
                if getSide(minimum + 1 + i, y) != 0:
                    return False
            return True
        return False


class Bishop(Piece):
    def validMove(self, x, y):
        if abs(self.x - x) == abs(self.y - y):
            xvec = -1
            if x - self.x > 0:
                xvec = 1
            yvec = -1
            if y - self.y > 0:
                yvec = 1
            magnitude = abs(self.x - x)
            xtest = self.x + xvec
            ytest = self.y + yvec
            while xtest != x and xtest < 9 and xtest > 0:
                if getSide(xtest, ytest) != 0:
                    return False
                xtest += xvec
                ytest += yvec
            return True
        return False


class Queen(Piece):
    def validMove(self, x, y):
        if self.x == x:
            minimum = min(self.y, y)
            maximum = max(self.y, y)
            for i in range(maximum - minimum - 1):
                if getSide(x, minimum + 1 + i) != 0:
                    return False
            return True
        elif self.y == y:
            minimum = min(self.x, x)
            maximum = max(self.x, x)
            for i in range(maximum - minimum - 1):
                if getSide(minimum + 1 + i, y) != 0:
                    return False
            return True
        elif abs(self.x - x) == abs(self.y - y):
            xvec = -1
            if x - self.x > 0:
                xvec = 1
            yvec = -1
            if y - self.y > 0:
                yvec = 1
            magnitude = abs(self.x - x)
            xtest = self.x + xvec
            ytest = self.y + yvec
            while xtest != x and xtest < 9 and xtest > 0:
                if getSide(xtest, ytest) != 0:
                    return False
                xtest += xvec
                ytest += yvec
            return True
        return False


class King(Piece):
    def validMove(self, x, y):
        if abs(self.x - x) <= 1 and abs(self.y - y) <= 1:
            if abs(self.x - x) == 0 and abs(self.y - y) == 0:
                return False
            return True
        return False


pygame.init()
pygame.display.set_caption("Chess")
screen = pygame.display.set_mode((800, 800))

# assigns pieces to the chessboard

pieces = []
for i in range(2):
    for j in range(2):
        pieces.append(Knight(i * 5 + 2, j * 7 + 1, (j - 0.5) * 2, pygame.image.load("knight.png")))
    for j in range(8):
        pieces.append(Pawn(j + 1, i * 5 + 2, (i - 0.5) * 2, pygame.image.load("pawn.png")))
    for j in range(2):
        pieces.append(Rook(j * 7 + 1, i * 7 + 1, (i - 0.5) * 2, pygame.image.load("rook.png")))
    for j in range(2):
        pieces.append(Bishop(j * 3 + 3, i * 7 + 1, (i - 0.5) * 2, pygame.image.load("bishop.png")))
    pieces.append(Queen(4, i * 7 + 1, (i - 0.5) * 2, pygame.image.load("queen.png")))
    pieces.append(King(5, i * 7 + 1, (i - 0.5) * 2, pygame.image.load("king.png")))

turn = 1

count = 0  # these variables are used in the ending screen
winner = 0

win_screen = []  # randomly determines what the end screen will look like
for i in range(8):
    for j in range(8):
        win_screen.append((i + 1, j + 1))
shuffle(win_screen)

done = False
selected = False

initialize()

while done == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # this code runs if the user clicks a cell and has not already selected something

        if event.type == pygame.MOUSEBUTTONDOWN and selected == False:
            xmouse1 = roundCell(pygame.mouse.get_pos()[0])
            ymouse1 = roundCell(pygame.mouse.get_pos()[1])
            for piece in pieces:
                if piece.x == xmouse1 and piece.y == ymouse1 and piece.alive and piece.side == turn:
                    origin_index = pieces.index(piece)
                    selected = True
                    drawBlank()
                    highlight()
                    shadeCell(sky, xmouse1, ymouse1)

            # this runs if there is a piece in the cell where the user first clicks

            if selected == True:
                for i in range(8):
                    for j in range(8):
                        if pieces[origin_index].validMove(i + 1, j + 1):  # marks possible moves, green for empty spaces and red for captures
                            if getSide(i + 1, j + 1) == 0:
                                shadeCell(forest, i + 1, j + 1)
                            elif getSide(i + 1, j + 1) != getSide(xmouse1, ymouse1):
                                shadeCell(red, i + 1, j + 1)
                            highlight()
            renderPieces()

        # this code runs if the user clicks a space after they have already selected something

        elif event.type == pygame.MOUSEBUTTONDOWN and selected == True:
            xmouse2 = roundCell(pygame.mouse.get_pos()[0])
            ymouse2 = roundCell(pygame.mouse.get_pos()[1])
            for piece in pieces:  #identifies what piece is in the selected square
                if piece.x == xmouse2 and piece.y == ymouse2 and piece.alive:
                    destination_index = pieces.index(piece)
            if pieces[origin_index].validMove(xmouse2, ymouse2) and (xmouse1 != xmouse2 or ymouse1 != ymouse2):  # if the move is valid
                if getSide(xmouse1, ymouse1) != getSide(xmouse2, ymouse2):  # checks to make sure the player is not trying to capture their own piece
                    if getSide(xmouse2, ymouse2) != 0:  # if
                        pieces[destination_index].alive = False
                        pieces[destination_index].side = 0
                    pieces[origin_index].x = xmouse2
                    pieces[origin_index].y = ymouse2
                    pieces[origin_index].moved = True
                    turn *= -1  # changes the turn if a valid move was made
            initialize()
            selected = False
    if pieces[15].alive == False and winner == 0:  # if the orange king is dead
        winner = 1
    elif pieces[31].alive == False and winner == 0:  # if the purple king is dead
        winner = -1
    if winner != 0 and count < 64:
        for piece in pieces:
            piece.alive = False
        shadeCell(player_colors[winner], win_screen[count][0], win_screen[count][1])
        count += 1
    pygame.display.update()
