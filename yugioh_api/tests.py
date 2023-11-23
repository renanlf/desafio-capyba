from rest_framework import status
from rest_framework.test import APITestCase

from yugioh_api.models import Player, Card
from django.contrib.auth.models import User

from datetime import datetime

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


class CardTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Card.objects.create(
            cid=1234567,
            title='Dark Magician',
            attribute='Dark',
            description='The ultimate wizard in terms of attack and defense.',
            attack=2500,
            defense=2100,
            release_date=datetime.strptime('2004-03-01', '%Y-%m-%d'),
        )
        Card.objects.create(
            cid=89631139,
            title='Blue-Eyes White Dragon',
            attribute='Light',
            description='This legendary dragon is a powerful engine of destruction. Virtually invincible, very few have faced this awesome creature and lived to tell the tale.',
            attack=3000,
            defense=2500,
            release_date=datetime.strptime('2004-03-01', '%Y-%m-%d'),
        )
        Card.objects.create(
            cid=93149655,
            title='Odd-Eyes Phantom Dragon',
            attribute='Dark',
            description="Pendulum Effect: Once per turn, when an attack is declared involving your face-up monster and an opponent's monster, if you have an \"Odd-Eyes\" card in your other Pendulum Zone: You can make that monster you control gain 1200 ATK until the end of the Battle Phase (even if this card leaves the field).\
Monster Effect: When this Pendulum Summoned card inflicts battle damage to your opponent by attacking: You can inflict damage to your opponent equal to the number of \"Odd-Eyes\" cards in your Pendulum Zones x 1200. You can only use this effect of \"Odd-Eyes Phantom Dragon\" once per turn.",
            attack=2500,
            defense=2000,
            release_date=datetime.strptime('2017-10-05', '%Y-%m-%d'),
        )

    def test_get_all(self):
        response = self.client.get('/cards/')
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(response.data['results'][0]['title'], 'Dark Magician')
        self.assertEqual(response.data['results'][1]['title'], 'Blue-Eyes White Dragon')
        self.assertEqual(response.data['results'][2]['title'], 'Odd-Eyes Phantom Dragon')

    def test_get_pagination(self):
        response = self.client.get('/cards/?page_size=2&page=2')
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(response.data['results'][0]['title'], 'Odd-Eyes Phantom Dragon')

    def test_get_search(self):
        response = self.client.get('/cards/?search=Dragon')
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['title'], 'Blue-Eyes White Dragon')
        self.assertEqual(response.data['results'][1]['title'], 'Odd-Eyes Phantom Dragon')

    def test_get_by_release_date(self):
        response = self.client.get('/cards/?release_date=2004-03-01')
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['title'], 'Dark Magician')
        self.assertEqual(response.data['results'][1]['title'], 'Blue-Eyes White Dragon')

    def test_get_ordering(self):
        response = self.client.get('/cards/?ordering=-release_date')
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(response.data['results'][0]['title'], 'Odd-Eyes Phantom Dragon')
        self.assertEqual(response.data['results'][1]['title'], 'Dark Magician')
        self.assertEqual(response.data['results'][2]['title'], 'Blue-Eyes White Dragon')


class EmailTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Player.objects.create(
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
        Player.objects.create(
            user=User.objects.create_user(
                username='renanlfTest2',
                email='renanlftest2@gmail.com',
                password='123456',
                first_name='Renan'
            ),
            pic=None,
            authenticated=True,
            token='token'
        )
        Player.objects.create(
            user=User.objects.create_user(
                username='renanlfTest3',
                email='renanlftest3@gmail.com',
                password='123456',
                first_name='Renan'
            ),
            pic=None,
            authenticated=False,
            token=''
        )
        Player.objects.create(
            user=User.objects.create_user(
                username='renanlfTest4',
                email='renanlftest4@gmail.com',
                password='123456',
                first_name='Renan'
            ),
            pic=None,
            authenticated=False,
            token=''
        )


    def test_get_confirmation(self):
        login_token = self.client.post('/login/', {
            'username': 'renanlfTest',
            'password': '123456',
        }).data['token']

        response = self.client.get('/confirmation/', {}, headers={
            "Authorization": f"Token {login_token}"
        })

        self.assertEqual(response.data['email'], 'renanlftest@gmail.com')
        self.assertTrue(response.data['link'].startswith('validate/?username=renanlfTest&token='))

    def test_get_confirmation_validated_email(self):
        login_token = self.client.post('/login/', {
            'username': 'renanlfTest2',
            'password': '123456',
        }).data['token']

        response = self.client.get('/confirmation/', {}, headers={
            "Authorization": f"Token {login_token}"
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, 'Email already validated')

    def test_post_validation(self):
        login_token = self.client.post('/login/', {
            'username': 'renanlfTest3',
            'password': '123456',
        }).data['token']

        validation_url = self.client.get('/confirmation/', headers={
            "Authorization": f"Token {login_token}"
        }).data['link']

        response = self.client.get(f"/{validation_url}", headers={
            "Authorization": f"Token {login_token}"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Email validated successfully!')

        response = self.client.get(f"/{validation_url}", headers={
            "Authorization": f"Token {login_token}"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, 'Email already validated')

    def test_post_validation_wrong_token(self):
        login_token = self.client.post('/login/', {
            'username': 'renanlfTest4',
            'password': '123456',
        }).data['token']

        validation_url = 'validate/?username=renanlfTest4&token=abcdef'

        response = self.client.get(f"/{validation_url}", headers={
            "Authorization": f"Token {login_token}"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Invalid token')

