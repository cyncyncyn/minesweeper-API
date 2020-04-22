from django.test import TestCase
from django.test import Client
from django.conf import settings


class APITestCase(TestCase):
    def test_board_is_returned(self):
        client = Client()
        response = client.get('/game/board/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), settings.BOARD)

    def test_game_ends_if_hitting_mine(self):
        client = Client()
        response = client.post('/game/click/', {"x":1,"y":2})
        self.assertEqual(response.status_code, 400)

    def test_game_returns_200_if_no_mine_hit(self):
        client = Client()
        response = client.post('/game/click/', {"x":3,"y":4})
        self.assertEqual(response.status_code, 200)

    def test_game_returns_adjacent_squares_if_no_mine_hit(self):
        client = Client()
        response = client.post('/game/click/', {"x":3,"y":4})
        self.assertEqual(response.status_code, 200)
