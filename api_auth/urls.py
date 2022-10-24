from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from api_auth import views as api_auth_view
from rest_framework.authtoken import views as auth_view

router = routers.DefaultRouter()
router.register(r'users', api_auth_view.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login', api_auth_view.LoginView.as_view()),
    path('logout', api_auth_view.LoginOutView.as_view()),
]

urlpatterns += [
    path('api-token-auth/', auth_view.obtain_auth_token)
]
