from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from yugioh_api.models import Player, Card, CardPrice

from drf_yasg import openapi


class RegisterSerializer(serializers.ModelSerializer):
    # reference: https://stackoverflow.com/questions/27804010/how-to-serialize-a-relation-onetoone-in-django-with-rest-framework
    email = serializers.EmailField(source='user.email', validators=[UniqueValidator(queryset=User.objects.all())], required=True)
    username = serializers.CharField(source='user.username', required=True)
    first_name = serializers.CharField(source='user.first_name', required=True)
    password = serializers.CharField(source='user.password', validators=[validate_password], required=True)

    class Meta:
        model = Player
        fields = ('id', 'email', 'username', 'first_name', 'password', 'pic')

    def create(self, validated_data):
        return Player.objects.create(
            user=User.objects.create_user(
                username=validated_data['user']['username'],
                email=validated_data['user']['email'],
                password=validated_data['user']['password'],
                first_name=validated_data['user']['first_name']
            ),
            pic=validated_data['pic'],
            authenticated=False,
            token='',
        )


class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = ['url', 'id', 'cid', 'title', 'description', 'attribute', 'attack', 'defense', 'release_date']


class CardPriceSerializer(serializers.HyperlinkedModelSerializer):
    card = CardSerializer()
    class Meta:
        model = CardPrice
        fields = ['card', 'min_price', 'max_price']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name']


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Player
        fields = ['url', 'id', 'user', 'pic']

