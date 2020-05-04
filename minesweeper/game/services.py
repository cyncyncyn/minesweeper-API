from game.models import Cell


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

    rowLimit = board.width
    colLimit = board.height

    cells_to_reveal = []
    neighbours_has_mine = []
    for i, j in surround_generator(x, y, rowLimit, colLimit):
        cell = board.cell_set.get(row=i, col=j)
        neighbours_has_mine.append(cell.is_mine)

    if any(neighbours_has_mine):
        return []
    else:
        for i, j in surround_generator(x, y, rowLimit, colLimit):
            if (i, j) in visited:
                continue

            cells_to_reveal.append((i, j))

            cell_object = Cell.objects.get(board=board, row=i, col=j)
            cell_object.is_uncovered = True
            cell_object.save()

            visited.append((i, j))
            recursive_adjacents = find_adjacents(board, i, j, visited)
            cells_to_reveal.extend(recursive_adjacents)

    return cells_to_reveal
