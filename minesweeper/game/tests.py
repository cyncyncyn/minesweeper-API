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
        pass
