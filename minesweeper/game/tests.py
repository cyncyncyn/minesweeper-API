from django.test import Client, TestCase

from game.services import find_adjacents
from game.models import Board


class APITestCase(TestCase):
    def get_cell_position(self, mine=True):
        """ Return first cell founds that matches mine param """
        amount_of_mines = 10 if mine else 0
        board = Board(width=10, height=10, amount_of_mines=amount_of_mines)
        board.generate_cells()
        for cell in board.cell_set.all():
            if mine and cell.is_mine:
                return cell
            if not mine and not cell.is_mine:
                return cell

    def setUp(self):
        client = Client()
        response = client.post('/game/board/')
        response_json = response.json()
        self.board_id = response_json["pk"]

    def test_board_is_returned(self):
        client = Client()
        response = client.get(f'/game/board/{self.board_id}/')

        self.assertEqual(response.status_code, 200)

        decoded_response = response.json()

        self.assertEqual(decoded_response['pk'], self.board_id)
        self.assertEqual(decoded_response['fields']['width'],
                         Board.DEFAULT_BOARD_SIZE)
        self.assertEqual(decoded_response['fields']['height'],
                         Board.DEFAULT_BOARD_SIZE)
        self.assertEqual(decoded_response['fields']['amount_of_mines'],
                         Board.DEFAULT_MINES_AMOUNT)
        self.assertEqual(decoded_response['fields']['status'], Board.PLAYING)

    def test_game_returns_400_if_hitting_mine(self):
        cell = self.get_cell_position(mine=True)
        client = Client()
        response = client.post(
            '/game/click/',
            {"x": cell.row, "y": cell.col, "boardId": cell.board.id},
            content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_game_returns_200_if_no_mine_hit(self):
        cell = self.get_cell_position(mine=False)
        client = Client()
        response = client.post(
            '/game/click/',
            {"x": cell.row, "y": cell.col, "boardId": cell.board.id},
            content_type="application/json")
        self.assertEqual(response.status_code, 200)


class FindAdjacentsWithoutMinesTestCase(TestCase):

    def setUp(self):
        board = Board(width=3, height=3, amount_of_mines=0)
        board.generate_cells()
        self.board = board

    def test_from_center(self):
        adjacents = set(find_adjacents(self.board, 1, 1))
        expected_adjacents = set(
            [
                (0, 0), (0, 1), (0, 2),
                (1, 0),         (1, 2),
                (2, 0), (2, 1), (2, 2)
            ]
        )

        self.assertEqual(adjacents, expected_adjacents)

    def test_from_right_bottom(self):
        adjacents = set(find_adjacents(self.board, 2, 2))
        expected_adjacents = set(
            [
                (0, 0), (0, 1), (0, 2),
                (1, 0), (1, 1), (1, 2),
                (2, 0), (2, 1)
            ]
        )

        self.assertEqual(adjacents, expected_adjacents)

    def test_from_right_top(self):
        adjacents = set(find_adjacents(self.board, 0, 2))
        expected_adjacents = set(
            [
                (0, 0), (0, 1),
                (1, 0), (1, 1), (1, 2),
                (2, 0), (2, 1), (2, 2)
            ]
        )

        self.assertEqual(adjacents, expected_adjacents)

    def test_from_left_bottom(self):
        adjacents = set(find_adjacents(self.board, 2, 0))
        expected_adjacents = set(
            [
                (0, 0), (0, 1), (0, 2),
                (1, 0), (1, 1), (1, 2),
                        (2, 1), (2, 2)
            ]
        )

        self.assertEqual(adjacents, expected_adjacents)


class FindAdjacentsWithMinesTestCase(TestCase):

    def test_from_left_bottom_with_mine_in_center(self):
        #    [False, False, False],
        #    [False, True,  False],
        #    [False, False, False],

        board = Board(width=3, height=3, amount_of_mines=0)
        board.generate_cells()
        cell_1_1 = board.cell_set.get(row=1, col=1)
        cell_1_1.is_mine = True
        cell_1_1.save()

        adjacents = set(find_adjacents(board, 2, 0))
        expected_adjacents = set([])

        self.assertEqual(adjacents, expected_adjacents)

    def test_from_left_bottom_with_mine_in_top_right(self):
        #    [False, False, True],
        #    [False, False, False],
        #    [False, False, False],
        board = Board(width=3, height=3, amount_of_mines=0)
        board.generate_cells()
        cell_1_1 = board.cell_set.get(row=0, col=2)
        cell_1_1.is_mine = True
        cell_1_1.save()

        adjacents = set(find_adjacents(board, 2, 0))
        expected_adjacents = set([
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 1),
            (1, 2),
            (2, 1),
            (2, 2)
        ])

        self.assertEqual(adjacents, expected_adjacents)

    def test_from_right_botom_with_mine_in_top_right(self):
        #    [True,  False, False],
        #    [False, False, False],
        #    [False, False, False],
        board = Board(width=3, height=3, amount_of_mines=0)
        board.generate_cells()
        cell_0_0 = board.cell_set.get(row=0, col=0)
        cell_0_0.is_mine = True
        cell_0_0.save()

        adjacents = set(find_adjacents(board, 2, 2))
        expected_adjacents = set([
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 1),
            (1, 2),
            (2, 0),
            (2, 1),
        ])

        self.assertEqual(adjacents, expected_adjacents)
