BOARD_SIZE = 8
def generate_board():
    board = []
    minesPosition = [
        (1,2),
        (3,2),
        (7,4),
        (4,6),
        (3,1),
        (0,8),
        (4,4),
        (7,8),
        (0,0),
        (2,2),
    ]
    for rowIndex in range (0, BOARD_SIZE):
        row = []
        for colIndex in range(0, BOARD_SIZE):
            hasMine = (rowIndex, colIndex) in minesPosition
            row.append(hasMine)
        board.append(row)
    return board


def find_adjacents(board, x, y):
    adjacents = []
    rowLimit = len(board)
    colLimit = len(board)

    for rowIndex in range(max(0, x -1), min(x + 1, rowLimit)):
        for colIndex in range(max(0, y-1), min(y + 1, colLimit)):
            if rowIndex != x and colIndex != y:
                if board[rowIndex][colIndex]:
                    return []
                recursive_adjacents = find_adjacents(board, rowIndex, colIndex)
                adjacents.extend(recursive_adjacents)
                adjacents.append((rowIndex, colIndex))
    return adjacents
