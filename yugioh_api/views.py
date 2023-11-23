from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from yugioh_api.models import Player, Card
from yugioh_api.serializers import RegisterSerializer, CardSerializer


class MyPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


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


class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cards to be viewed or edited if authenticated.
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = MyPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['cid', 'release_date', 'attribute']
    ordering_fields = ['release_date', 'cid', 'title']