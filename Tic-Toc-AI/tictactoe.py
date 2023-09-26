import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_COLOR = (0, 0, 0)
LINE_WIDTH = 15
BOARD_SIZE = 3
SQUARE_SIZE = WIDTH // BOARD_SIZE
PLAYER_X = 1
PLAYER_O = 2
EMPTY = 0

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Initialize the board
board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]

# Draw the grid
def draw_grid():
    for row in range(1, BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (row * SQUARE_SIZE, 0), (row * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Draw X and O on the board
def draw_symbols():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == PLAYER_X:
                pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE),
                                 ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
                pygame.draw.line(screen, LINE_COLOR, ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE),
                                 (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
            elif board[row][col] == PLAYER_O:
                pygame.draw.circle(screen, LINE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - LINE_WIDTH // 2, LINE_WIDTH)

# Check if a player has won
def check_win(player):
    for row in range(BOARD_SIZE):
        if all([board[row][col] == player for col in range(BOARD_SIZE)]):  # Check rows
            return True
    for col in range(BOARD_SIZE):
        if all([board[row][col] == player for row in range(BOARD_SIZE)]):  # Check columns
            return True
    if all([board[i][i] == player for i in range(BOARD_SIZE)]) or \
       all([board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)]):  # Check diagonals
        return True
    return False

# Check if the board is full (draw)
def is_draw():
    return all(board[i][j] != EMPTY for i in range(BOARD_SIZE) for j in range(BOARD_SIZE))

# Minimax algorithm with Alpha-Beta Pruning
def minimax(board, depth, is_maximizing):
    if check_win(PLAYER_X):
        return -1
    if check_win(PLAYER_O):
        return 1
    if is_draw():
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER_O
                    eval = minimax(board, depth + 1, False)
                    board[row][col] = EMPTY
                    max_eval = max(max_eval, eval)
        return max_eval

    else:
        min_eval = math.inf
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER_X
                    eval = minimax(board, depth + 1, True)
                    board[row][col] = EMPTY
                    min_eval = min(min_eval, eval)
        return min_eval

# Find the best move using Minimax with Alpha-Beta Pruning
def find_best_move(board):
    best_eval = -math.inf
    best_move = None
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY:
                board[row][col] = PLAYER_O
                eval = minimax(board, 0, False)
                board[row][col] = EMPTY
                if eval > best_eval:
                    best_eval = eval
                    best_move = (row, col)
    return best_move

# Main game loop
turn = PLAYER_X
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if turn == PLAYER_X and not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER_X
                    if check_win(PLAYER_X):
                        game_over = True
                    elif is_draw():
                        game_over = True
                    else:
                        turn = PLAYER_O

        elif turn == PLAYER_O and not game_over:
            row, col = find_best_move(board)
            if board[row][col] == EMPTY:
                board[row][col] = PLAYER_O
                if check_win(PLAYER_O):
                    game_over = True
                elif is_draw():
                    game_over = True
                else:
                    turn = PLAYER_X

    screen.fill((255, 255, 255))
    draw_grid()
    draw_symbols()
    pygame.display.update()

pygame.time.delay(2000)  # Pause for 2 seconds after game over
pygame.quit()
sys.exit()

