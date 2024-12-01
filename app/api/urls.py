from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserAuthViewSet


app_name = 'api'

router = DefaultRouter()

router.register('users', UserAuthViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]