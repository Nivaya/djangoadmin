from django.urls import path, include
from django.contrib.auth.models import User, Group
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from rest_framework import routers, serializers, viewsets


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username", write_only=True)
    password = serializers.CharField(label="Password",
                                     style={'input_type': 'password'},
                                     trim_whitespace=False,
                                     write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ResponseSerializer(serializers.Serializer):
    errcode = serializers.BooleanField()
    errmsg = serializers.CharField(max_length=50)
    data = serializers.JSONField()
