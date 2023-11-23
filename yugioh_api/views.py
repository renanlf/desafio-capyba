from rest_framework import generics, permissions
from django.contrib.auth.models import User

from yugioh_api.models import Player
from yugioh_api.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = Player.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
