from rest_framework import status
from rest_framework.test import APITestCase

from yugioh_api.models import Player
from django.contrib.auth.models import User


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

    def test_policies(self):
        response = self.client.get('/policy/')
        self.assertEqual(response.get('Content-Disposition'), 'attachment; filename="policies.pdf"')
    def test_login(self):
        """
        Ensure we can login
        """
        player = Player.objects.create(
            user=User.objects.create_user(
                username='renanlfTest',
                email='renanlftest@gmail.com',
                password='123456',
                first_name='Renan'
            ),
            pic=None,
            authenticated=False,
            token=''
        )
        player.save()

        response = self.client.post('/login/', {
            'username': 'renanlfTest',
            'password': '12345',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data), "{'non_field_errors': [ErrorDetail(string='Unable to log in with provided credentials.', code='authorization')]}")

        response = self.client.post('/login/', {
            'username': 'renanlfTest',
            'password': '123456',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)