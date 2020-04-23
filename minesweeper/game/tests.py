from django.test import Client, TestCase

from .services import BOARD_SIZE, find_adjacents


class APITestCase(TestCase):
    # TODO: board is hardcoded for this demo version
    # After this version we should use a random board and select
    # a coord with each case (coord with adjacent mine, coord with mine,
    #  coord with no adjacent mine)
    def test_board_is_returned(self):
        client = Client()
        response = client.get('/game/board/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'size': BOARD_SIZE})

    def test_game_ends_if_hitting_mine(self):
        client = Client()
        response = client.post(
            '/game/click/', '{"x":1,"y":2}'.encode('utf-8'),
            content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_game_returns_200_if_no_mine_hit(self):
        client = Client()
        response = client.post(
            '/game/click/', '{"x":3,"y":4}'.encode('utf-8'),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_returns_empty_adjacents_if_no_mine_hit_but_mine_is_neighbour(self):
        client = Client()
        coord_with_adjacent_mine = '{"x": 3,"y": 4}'
        response = client.post(
            '/game/click/', coord_with_adjacent_mine.encode('utf-8'),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_returns_adjacents_if_no_mine_hit(self):
        client = Client()
        coord_with_adjacent_mine = '{"x": 7,"y": 7}'
        response = client.post(
            '/game/click/', coord_with_adjacent_mine.encode('utf-8'),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), [
                [6, 6], [5, 5], [5, 6], [5, 7], [6, 5], [6, 7], [7, 6], [7, 5]
            ]
        )


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
