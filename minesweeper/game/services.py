def generate_random_board():
    # 8 * 8
    # 10 mines
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
    for row in range (0,9):
        for cell in range(0,9):
            mine = (row, cell) in minesPosition
            board.append({
                "x":row,
                "y": cell,
                "mine": mine
            })


    return board
