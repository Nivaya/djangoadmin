from django.shortcuts import render
from django.contrib.auth import (
    authenticate, get_user_model, password_validation, login, logout
)
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from api_auth.serializers import LoginSerializer, UserSerializer, GroupSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie

from django.contrib.auth.models import User, Group
from django.contrib import admin

admin.autodiscover()
from rest_framework import generics, permissions, serializers
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


# class UserViewSet(viewsets.ModelViewSet):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class LoginView(APIView):

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content, status=status.HTTP_200_OK)


class LoginOutView(APIView):

    def post(self, request, format=None):
        logout(request)
        return Response(None, status=status.HTTP_200_OK)


# Create the API views
class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
