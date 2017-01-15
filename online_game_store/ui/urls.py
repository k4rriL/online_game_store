"""online_game_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r"^games/success", views.game_purchase_success, name='success'),
    url(r"^addnewgame/", views.add_new_game, name="addnewgame"),
    url(r"^game/(?P<gameId>\w+)$", views.game_info, name='game'),
    url(r"^category/(?P<category>\w+)$", views.category, name='category'),
    url(r"^$", views.front, name='home'),
]
