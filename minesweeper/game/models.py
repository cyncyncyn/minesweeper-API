import uuid
import random

from django.db import models


BOARD_SIZE = 8
MINES_AMOUNT = 10


class Board(models.Model):
    PLAYING = "PLY"
    WON = "WON"
    LOST = "LST"
    status = (
        (PLAYING, "Playing"),
        (WON, "Won"),
        (LOST, "Lost"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    width = models.PositiveIntegerField(default=BOARD_SIZE)
    height = models.PositiveIntegerField(default=BOARD_SIZE)
    amount_of_mines = models.PositiveIntegerField(default=MINES_AMOUNT)
    status = models.CharField(choices=status, max_length=3, default=PLAYING)

    # TODO: fix the repeated mines
    def generate_random_mines(self, amount_of_mines):
        return [
           (
               random.randrange(0, BOARD_SIZE),
               random.randrange(0, BOARD_SIZE)
           ) for _ in range(amount_of_mines)
        ]

    def generate_cells(self):
        random_mines = self.generate_random_mines(self.amount_of_mines)
        board = []
        for rowIndex in range(0, self.width):
            row = []
            for colIndex in range(0, self.height):
                is_mine = (rowIndex, colIndex) in random_mines
                cell = Cell(
                    board=self, row=rowIndex, col=colIndex, is_mine=is_mine)
                super(Board, self).save()

                cell.save()
                row.append(cell)
            board.append(row)
        return board


class Cell(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    row = models.PositiveIntegerField()
    col = models.PositiveIntegerField()
    flagged = models.BooleanField(default=False)
    is_mine = models.BooleanField(default=False)
