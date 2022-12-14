from django.shortcuts import render
from django.contrib.auth import (
    authenticate, get_user_model, password_validation, login, logout
)
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from api_auth.serializers import UserSerializer, LoginSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        content = {
            'errcode': 0,
            'errmsg': None,
            'data': {
                'user': str(request.user),
            }
        }
        return Response(content, status=status.HTTP_200_OK)


class LoginOutView(APIView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)
