BOARD_SIZE = 8


def generate_board(random_mines):
    board = []
    for rowIndex in range(0, BOARD_SIZE):
        row = []
        for colIndex in range(0, BOARD_SIZE):
            hasMine = (rowIndex, colIndex) in random_mines
            row.append(hasMine)
        board.append(row)
    return board


def generate_boards():
    boards = []
    for x in range(10):
        import random
        random_mines = [
            (
                random.randrange(0, BOARD_SIZE),
                random.randrange(0, BOARD_SIZE)
            ) for i in range(10)
         ]
        boards.append(generate_board(random_mines))

    return boards


def cell_has_mine(board, x, y):
    return board[x][y]


def surround_generator(x, y, max_row, max_col):
    for i in range(max(0, x-1), min(x+2, max_row)):
        for j in range(max(0, y-1), min(y+2, max_col)):
            if x != i or y != j:
                yield (i, j)


def find_adjacents(board, x, y, visited=None):
    visited = visited or []
    visited.append((x, y))

    rowLimit = len(board)
    colLimit = len(board[0])

    cells_to_reveal = []
    has_mine = False
    neighbours_has_mine = []
    for i, j in surround_generator(x, y, rowLimit, colLimit):
        has_mine = board[i][j]
        neighbours_has_mine.append(has_mine)

    if any(neighbours_has_mine):
        return []
    else:
        for i, j in surround_generator(x, y, rowLimit, colLimit):
            if (i, j) in visited:
                continue

            cells_to_reveal.append((i, j))
            visited.append((i, j))
            recursive_adjacents = find_adjacents(board, i, j, visited)
            cells_to_reveal.extend(recursive_adjacents)

    return cells_to_reveal
