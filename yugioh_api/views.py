from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets, status
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from yugioh_api.models import Player, Card, CardPrice
from yugioh_api.serializers import RegisterSerializer, CardSerializer, CardPriceSerializer, PlayerSerializer


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


class EmailConfirmationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        player = Player.objects.get(user=request.user)

        if player.authenticated:
            return Response('Email already validated', status=status.HTTP_403_FORBIDDEN)

        confirmation_token = default_token_generator.make_token(request.user)
        player.token = confirmation_token
        player.save()
        return Response({
            "email": request.user.email,
            "link": f'validate/?username={request.user.username}&token={confirmation_token}'
        })


class EmailValidationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        #reference: https://stackoverflow.com/questions/64375033/email-verification-django-rest-framework
        token = request.query_params.get('token', '')

        player = Player.objects.get(user=request.user)

        if player.authenticated:
            return Response('Email already validated', status=status.HTTP_403_FORBIDDEN)

        if player.token == token:
            player.authenticated = True
            player.save()
            return Response('Email validated successfully!', status=status.HTTP_200_OK)
        else:
            return Response('Invalid token', status=status.HTTP_400_BAD_REQUEST)

class CardPriceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows card prices to be viewed or edited if authenticated.
    """
    queryset = CardPrice.objects.all()
    serializer_class = CardPriceSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MyPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['card__title', 'card__description']
    filterset_fields = ['card__cid', 'card__release_date', 'card__attribute', 'min_price', 'max_price']
    ordering_fields = ['card__release_date', 'card__cid', 'card__title', 'min_price', 'max_price']

class PlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows players to be viewed or edited if admin user.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAdminUser]