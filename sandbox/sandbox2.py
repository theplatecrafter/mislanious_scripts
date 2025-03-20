test_string = ''
try:
    if test_string[0] == 'O':
        print("O found")
except IndexError as e:
    print(f"IndexError: {e}")
    print(f"test_string: {test_string}")

board = [[['' for _ in range(3)] for _ in range(3)] for _ in range(3)]
print(board)

try:
    if board[0][0][0][0] == 'O':
        print("O found")
except IndexError as e:
    print(f"IndexError: {e}")
    print(f"board[0][0][0][0]: {board[0][0][0]}")