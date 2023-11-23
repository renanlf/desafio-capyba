from django.http import HttpResponse
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.views import APIView

from yugioh_api.models import Player
from yugioh_api.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = Player.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class PolicyView(APIView):
    def get(self, request):
        #reference: https://stackoverflow.com/questions/30438729/how-do-i-use-django-rest-framework-to-send-a-file-in-response
        with open("policies.pdf", errors='replace') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "policies.pdf"
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

            return response
