from django.test import TestCase
from django.test import Client
from django.conf import settings


from .services import BOARD_SIZE, find_adjacents # TODO: this should be a setting

class APITestCase(TestCase):
    def test_board_is_returned(self):
        client = Client()
        response = client.get('/game/board/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'size': BOARD_SIZE})

    def test_game_ends_if_hitting_mine(self):
        client = Client()
        response = client.post('/game/click/', '{"x":1,"y":2}'.encode('utf-8'), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_game_returns_200_if_no_mine_hit(self):
        client = Client()
        response = client.post('/game/click/', '{"x":3,"y":4}'.encode('utf-8'), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_game_returns_adjacent_squares_if_no_mine_hit(self):
        client = Client()
        response = client.post('/game/click/', {"x":3,"y":4})
        self.assertEqual(response.status_code, 200)

class ServiceTestCase(TestCase):
    def test_find_adjacents(self):
        board = [
            [False, False, False],
            [False, False, False],
            [False, False, False],
        ]

        adjacents = set(find_adjacents(board, 1,1))
        expected_adjacents = set(
            [(0,0), (0,1), (0,2),
            (1,0),         (1,2),
            (2,0), (2,1),  (2,2)
            ]
        )

        self.assertEqual(adjacents, expected_adjacents)