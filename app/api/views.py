from django.core.cache import cache
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import User

from .serializers import (AuthSerializer, OTPSerializer, ReferalSerializer,
                          UserSerializer)
from .utils import generate_otp_code


class UserAuthViewSet(mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'send_otp':
            return OTPSerializer
        if self.action == 'auth':
            return AuthSerializer
        if self.action in ('me', 'retrieve'):
            return UserSerializer
        if self.action == 'referal':
            return ReferalSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ('me', 'retrieve', 'referal'):
            return (IsAuthenticated(),)
        return super().get_permissions()

    @action(
        methods=['POST'],
        detail=False,
        url_path='send_otp'
    )
    def send_otp(self, request):
        """Метод отправки 4-значного кода в смс."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otp = generate_otp_code()
            cache.set(
                key=otp,
                value=serializer.validated_data['phone_number'],
                timeout=300
            )
            serializer.validated_data['otp'] = otp
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['POST'],
        detail=False,
        url_path='auth'
    )
    def auth(self, request):
        """Авторизация/регистрация через подтверждающий код из смс."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = cache.get(
                key=serializer.validated_data['otp']
            )
            if phone_number:
                user, created = User.objects.get_or_create(phone_number=phone_number)
                token, created = Token.objects.get_or_create(user=user)
                serializer.validated_data['phone_number'] = user.phone_number
                serializer.validated_data['token'] = token
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Your otp code is wrong!'}, status=status.HTTP_400_BAD_REQUEST)

    @action(["get"], detail=False, url_path='me')
    def me(self, request, *args, **kwargs):
        """Личная страница пользователя."""
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(["post"], detail=False, url_path='referal')
    def referal(self, request, *args, **kwargs):
        """Указание реферального кода."""
        user = request.user
        serializer = self.get_serializer(data=request.data, instance=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
