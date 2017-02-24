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
    url(r"^games/$", views.games_json, name='games'),
    url(r"^v1/games/$", views.game_list, name='game_list'),
    url(r"^v1/games/(?P<gameid>\w+)$", views.game, name='gameid'),
    url(r"^v1/highscores/(?P<gameid>\w+)$", views.highscores, name='highscores'),
    url(r'^v1/salenumbers/$', views.sales_numbers, name='sales_numbers'),
]
