import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // 9
LINE_WIDTH = 5
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 5
CROSS_WIDTH = 5
CROSS_PADDING = CELL_SIZE // 4
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (0, 0, 255)
CROSS_COLOR = (255, 0, 0)
WIN_COLOR = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Tic-Tac-Toe")

# Game state
board = [[['' for _ in range(3)] for _ in range(3)] for _ in range(3)]
big_board = [['' for _ in range(3)] for _ in range(3)]
current_player = 'X'
last_move = None
game_over = False
winner = None

# Helper functions
def draw_board():
    screen.fill(BG_COLOR)
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * 3 * CELL_SIZE, 0), (i * 3 * CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * 3 * CELL_SIZE), (WIDTH, i * 3 * CELL_SIZE), LINE_WIDTH)
    for i in range(9):
        if i % 3 != 0:
            pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)
        if i >= 3:
            pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)

def draw_pieces():
    try:
        if board[0][0][0][0] == 'O':
            print("O found")
        elif board[0][0][0][0] == 'X':
            print("X found")
    except IndexError as e:
        print(f"IndexError in draw_pieces: {e}")
        print(f"board[0][0][0][0]: {board[0][0][0][0]}")

def check_win(board_to_check):
    for i in range(3):
        if board_to_check[i][0] == board_to_check[i][1] == board_to_check[i][2] != '':
            return board_to_check[i][0]
        if board_to_check[0][i] == board_to_check[1][i] == board_to_check[2][i] != '':
            return board_to_check[0][i]
    if board_to_check[0][0] == board_to_check[1][1] == board_to_check[2][2] != '':
        return board_to_check[0][0]
    if board_to_check[0][2] == board_to_check[1][1] == board_to_check[2][0] != '':
        return board_to_check[0][2]
    if all(board_to_check[row][col] != '' for row in range(3) for col in range(3)):
        return 'Tie'
    return None

def check_big_win():
    global game_over, winner
    result = check_win(big_board)
    if result:
        game_over = True
        winner = result
        if winner == 'Tie':
            print("It's a tie!")
        else:
            print(f"Player {winner} wins!")

def handle_click(pos):
    global current_player, last_move
    if game_over:
        return

    col = pos[0] // CELL_SIZE
    row = pos[1] // CELL_SIZE
    big_col = col // 3
    big_row = row // 3
    small_col = col % 3
    small_row = row % 3

    if last_move:
        if last_move[0] != big_row or last_move[1] != big_col:
            if big_board[last_move[0]][last_move[1]] != '':
                pass
            elif big_board[big_row][big_col] != '':
                pass
            else:
                return

    if board[big_row][big_col][small_row][small_col] == '':
        board[big_row][big_col][small_row][small_col] = current_player
        result = check_win(board[big_row][big_col])
        if result:
            big_board[big_row][big_col] = result
            check_big_win()
        current_player = 'O' if current_player == 'X' else 'X'
        last_move = (small_row, small_col)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                handle_click(event.pos)

    draw_board()
    draw_pieces()
    pygame.display.flip()

pygame.quit()
sys.exit()