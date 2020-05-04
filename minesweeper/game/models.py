import uuid
import random

from django.db import models


class Board(models.Model):
    DEFAULT_BOARD_SIZE = 8
    DEFAULT_MINES_AMOUNT = 10

    PLAYING = "PLY"
    WON = "WON"
    LOST = "LST"
    status = (
        (PLAYING, "Playing"),
        (WON, "Won"),
        (LOST, "Lost"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    width = models.PositiveIntegerField(default=DEFAULT_BOARD_SIZE)
    height = models.PositiveIntegerField(default=DEFAULT_BOARD_SIZE)
    amount_of_mines = models.PositiveIntegerField(default=DEFAULT_MINES_AMOUNT)
    status = models.CharField(choices=status, max_length=3, default=PLAYING)

    # TODO: fix the repeated mines
    def generate_random_mines(self, amount_of_mines):
        return [
           (
               random.randrange(0, self.width),
               random.randrange(0, self.height)
           ) for _ in range(self.amount_of_mines)
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
    is_flagged = models.BooleanField(default=False)
    is_mine = models.BooleanField(default=False)
    is_uncovered = models.BooleanField(default=False)
