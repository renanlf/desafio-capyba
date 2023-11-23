"""
URL configuration for desafio_capyba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from yugioh_api import views

router = routers.DefaultRouter()
router.register(r'cards', views.CardViewSet, basename='card')

urlpatterns = [
    path('auth/', include('rest_framework.urls')),  # to authenticate and use DRF admin
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('policy/', views.PolicyView.as_view(), name='policy'),
    path('login/', obtain_auth_token),
    path('', include(router.urls)),
]
