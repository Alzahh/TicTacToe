# To run this code you need to install pygame
# if your python version is almost 3 you can use pip
# If you need help with using pip, here is a link
# https://stackoverflow.com/questions/31968738/how-do-i-install-pygame-with-pip-in-python-3-4
import pygame
from sys import exit
from math import inf
from copy import deepcopy
pygame.init()
win = pygame.display.set_mode([330, 350])
pygame.display.set_caption("Tic Tac Toe AI")


# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
Blue = (0, 0, 255)
RED = (255, 0, 0)


win.fill(BLACK)


game = True
Human = False
Comp = True
RECT = [] # mass of fields

# restart buttoms
restartX = pygame.draw.rect(win, BLACK, [10, 10, 130, 30], 0)
restartO = pygame.draw.rect(win, BLACK, [180, 10, 130, 30], 0)
font = pygame.font.SysFont("Consolas", 25, 0, 0)
X_label = font.render("Restart X", 1, Blue)
Y_label = font.render("Restart O", 1, RED)

Win_matrix = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


def reset(mark):
    side = 70
    x = 50
    y = 60
    margin = 10
    global game, Hum_index, Comp_index, state, Comp_color, Hum_color
    game = True

    for Row in range(9):
        rectangle = pygame.draw.rect(win, WHITE, [x, y, side, side], 0)
        RECT.append(rectangle)
        x += side + margin
        if (Row + 1) % 3 == 0:
            y += side + margin
            x = 50
    if mark == "X":
        Hum_color = Blue
        Comp_color = RED
        Hum_index = -1
        Comp_index = 1

        return [0, 0, 0, 0, 0, 0, 0, 0, 0]
    else:
        Hum_color = RED
        Comp_color = Blue
        Hum_index = 1
        Comp_index = -1
        state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        AI(state, 0, Comp, -inf, inf)
        return state


state = reset("X")


# check the board via win_matrix
def win_check(board, player):
    if player == Human:
        value = Hum_index
    else:
        value = Comp_index
    for x in range(8):
        win = True       # возможен говнокод!!!
        for y in range(3):
            if board[Win_matrix[x][y]] != value:
                win = False
                break
        if win:
            return True
    return False

# check if the board is full
def board_check(board):
    for item in board:
        if item == 0:
            return False
    return True


# This def see what will happen in different situations. It create several branches of possible moves, analise them
# and add heuristic value

def AI(board, depth, player, alpha, beta):
    if win_check(board, not player):
        return -10 + depth   # heuristic value is - 10 plus depth because ideal player should win as fast as can
    if board_check(board):   # and do mo loose as long as possible
        return 0
    if player == Human:
        value = Hum_index
    else:
        value = Comp_index
    best = -inf
    grid = 0
    for x in range(9):
        if board[x] == 0:
            new_board = deepcopy(board)
            new_board[x] = value
            # negamax make code simplier via  via recursion
            move_value = -AI(new_board, depth + 1, not player, - beta, - alpha)
            if move_value > best:
                best = move_value
                grid = x
            # alpha- beta pruning stops analysing branch if there one one unsuitable value
            if move_value > alpha:
                alpha = move_value
            if alpha >= beta:
                return alpha
    if depth == 0:
        # change grid value and fill it
        state[grid] = Comp_index
        RECT[grid] = pygame.draw.rect(win, Comp_color, [RECT[grid][0], RECT[grid][1], RECT[grid][2], RECT[grid][3]], 0)
    return best


# -------- Main Program Loop -----------
# It is usual pygame loop, which render objects and get events
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for row in range(9):
                if RECT[row].collidepoint(pos):
                    if state[row] == 0 and game == True:
                        state[row] = Hum_index
                        RECT[row] = pygame.draw.rect(win, Hum_color, [RECT[row][0], RECT[row][1], RECT[row][2], RECT[row][3]], 0)
                        if win_check(state, Human):
                            game = False
                        AI(state, 0, Comp, -inf, inf)
                        if win_check(state, Comp):
                            game = False
                elif restartX.collidepoint(pos):
                    pygame.display.set_caption("You play X")
                    state = reset("X")
                elif restartO.collidepoint(pos):
                    pygame.display.set_caption("You play O")
                    state = reset("O")
    win.blit(X_label, (10, 10))
    win.blit(Y_label, (190, 10))
    pygame.display.flip()