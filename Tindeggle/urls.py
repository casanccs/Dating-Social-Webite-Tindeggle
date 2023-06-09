"""Tindeggle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from match.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', HomeView, name='HomeView'),
    path('createProfile/', CreateProfileView, name='createProfile'),
    path('addInterests/', AddInterestsView, name='addInterests'),
    path('editInterests/', EditInterestsView, name='editInterests'),
    path('profileSearch/', ProfileSearchView, name='profileSearch'),
    path('profileView/<str:username>/', ProfileView, name='profileView'),
    path('chat/<str:username1>/<str:username2>/', ChatView, name='chatView'),
    path('startChat/', StartChatView, name='startChat'),
    path('randomChat/<int:id>', RandomChatView, name='RandomChat'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
