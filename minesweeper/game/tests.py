from django.test import Client, TestCase

from .services import BOARD_SIZE, find_adjacents


from django.conf import settings


class APITestCase(TestCase):
    BOARD_ID = 0
    BOARD = settings.BOARDS[BOARD_ID]

    def get_cell_position(self, mine=True):
        """ Returns first cell founds that matches mine param """
        for i, row in enumerate(self.BOARD):
            for j, col in enumerate(row):
                if col == mine:
                    return i, j

    def test_board_is_returned(self):
        client = Client()
        response = client.get('/game/board/')

        self.assertEqual(response.status_code, 200)

        decoded_response = response.json()
        self.assertEqual(decoded_response['boardSize'], BOARD_SIZE)
        self.assertIn(decoded_response['boardId'], range(len(settings.BOARDS)))

    def test_game_returns_400_if_hitting_mine(self):
        x, y = self.get_cell_position(mine=True)
        client = Client()
        response = client.post(
            '/game/click/', {"x": x, "y": y, "boardId": self.BOARD_ID},
            content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_game_returns_200_if_no_mine_hit(self):
        x, y = self.get_cell_position(mine=False)
        client = Client()
        response = client.post(
            '/game/click/', {"x": x, "y": y, "boardId": self.BOARD_ID},
            content_type="application/json")
        self.assertEqual(response.status_code, 200)


class FindAdjacentsWithoutMinesTestCase(TestCase):

    board = [
            [False, False, False],
            [False, False, False],
            [False, False, False],
    ]

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
        board = [
            [False, False, False],
            [False, True,  False],
            [False, False, False],
        ]

        adjacents = set(find_adjacents(board, 2, 0))
        expected_adjacents = set([])

        self.assertEqual(adjacents, expected_adjacents)

    def test_from_left_bottom_with_mine_in_top_right(self):
        board = [
            [False, False, True],
            [False, False, False],
            [False, False, False],
        ]

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
        board = [
            [True,  False, False],
            [False, False, False],
            [False, False, False],
        ]

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
