from rest_framework import status
from rest_framework.test import APITestCase


class RegisterLoginPlayerTests(APITestCase):
    def test_register_player(self):
        """
        Ensure we can register a new player
        :return:
        """
        response = self.client.post('/register/', {
            "email": "yugi@yugioh.com",
            'username': 'yugi',
            'first_name': 'Yugi',
            'password': 'seNHAdoTeste123@'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with open('yugi.jpeg', 'rb') as pic:
            response = self.client.post('/register/', {
                "email": "yugi@yugioh.com",
                'username': 'yugi',
                'first_name': 'Yugi',
                'password': 'seNHAdoTeste123@',
                'pic': pic,
                'authenticated': False,
                'token': '',
            })
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

