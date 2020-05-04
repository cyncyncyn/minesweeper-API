from game.models import Board


def create_game(width, height, amount_of_mines):
    board = Board(width=width, height=height,
                  amount_of_mines=amount_of_mines)

    board.save()
    board.generate_cells()
    return board


def get_cell(data):
    x = int(data["x"])
    y = int(data["y"])
    board_id = data["boardId"]

    board = Board.objects.get(pk=board_id, status=Board.PLAYING)
    cell = board.cell_set.get(row=x, col=y)
    return cell


def uncover_cells(cells, adjacents):
    for cell in cells:
        if (cell.row, cell.col) in adjacents:
            cell.is_uncovered = True
            cell.save()


def board_to_list(board, cells):
    board_list = []

    min = 0
    max = 8
    for _ in range(board.width):
        row = []
        for c in cells[min:max]:
            row.append(c.is_mine)
        board_list.append(row)
        min = min + board.width
        max = min + board.width
    return board_list


def validate_game_finished(board):
    total_cells_discovered = board.cell_set.filter(is_uncovered=True).count()
    total_cells = board.width * board.height

    if total_cells_discovered + board.amount_of_mines == total_cells:
        return True
    return False


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
