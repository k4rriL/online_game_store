from django.test import TestCase
from django.urls import reverse
from django.db import connection
from gamedata.models import Game, Player, Developer, GamesOfPlayer
from django.contrib.auth.models import User
from django.test import TransactionTestCase, Client
from . import views
import json
from rest_framework.authtoken.models import Token



class GameDataViewTests(TestCase):



    def test_game_list(self):

        #Define some test data
        user_for_dev = User.objects.create_user(username="testdev", password="testpass")
        developer = Developer.objects.create(user=user_for_dev)
        game = Game.objects.create(name="test game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")
        game2 = Game.objects.create(name="test2 game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")

        client = Client()
        #Check that the response contains correct
        #information about these two games
        response = client.get("/api/v1/games/")
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)

        #Check that the response contains correct
        #information about these two games
        self.assertEqual(as_json[0]["id"], game.id)
        self.assertEqual(as_json[0]["name"], game.name)
        self.assertEqual(as_json[0]["price"], game.price)
        self.assertEqual(as_json[0]["category"], game.category)

        self.assertEqual(as_json[1]["id"], game2.id)
        self.assertEqual(as_json[1]["name"], game2.name)
        self.assertEqual(as_json[1]["price"], game2.price)
        self.assertEqual(as_json[1]["category"], game2.category)


    def test_game(self):

        #Define some test data
        user_for_dev = User.objects.create_user(username="testdev", password="testpass")
        developer = Developer.objects.create(user=user_for_dev)
        game = Game.objects.create(name="test game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")

        client = Client()
        #Check that the response contains correct
        #information about these two games
        response = client.get("/api/v1/games/" + str(game.id))
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)

        #Check that the response contains correct
        #information about this game
        self.assertEqual(as_json["id"], game.id)
        self.assertEqual(as_json["name"], game.name)
        self.assertEqual(as_json["price"], game.price)
        self.assertEqual(as_json["category"], game.category)

        response = client.get("/api/v1/games/1" + str(game.id))
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)

        #Check that with a wrong id, the response is empty
        self.assertEqual(as_json, "{}")



    def test_highscores(self):

        #Define some test data
        user_for_dev = User.objects.create_user(username="testdev", password="testpass")
        user_for_player = User.objects.create_user(username="testplayer", password="testpass")
        developer = Developer.objects.create(user=user_for_dev)
        player = Player.objects.create(user=user_for_player)
        game = Game.objects.create(name="test game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")
        game_of_player = GamesOfPlayer.objects.create(game=game, user=player, highscore="100", gameState="assdf")

        #Create client and make GET request
        client = Client()
        response = client.get("/api/v1/highscores/" + str(game.id))
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)

        #Check that the response contains correct
        #information about this game's highscores
        self.assertEqual(as_json[0]["user"], "testplayer")
        self.assertEqual(as_json[0]["highscore"], 100)

        #Check that response is correct with invalid game id
        response = client.get("/api/v1/highscores/1" + str(game.id))
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)

        #Check that the response contains correct
        #information about this game
        self.assertEqual(as_json, "[]")



    def test_salenumbers(self):

        #Define some test data
        user_for_dev = User.objects.create_user(username="testdev", password="testpass")
        user_for_player = User.objects.create_user(username="testplayer", password="testpass")
        developer = Developer.objects.create(user=user_for_dev)
        player = Player.objects.create(user=user_for_player)
        game = Game.objects.create(name="test game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")


        token = Token.objects.get(user=user_for_dev)

        #Create client and make GET request
        client = Client()
        response = client.get("/api/v1/salenumbers/")
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)

        #Check that the sale numbers are unavailable if
        #correct HTTP headers are not given
        self.assertEqual(as_json["detail"], "Authentication credentials were not provided.")

        #Make GET request with correct headers
        response = client.get("/api/v1/salenumbers/", HTTP_AUTHORIZATION="Token " + str(token))
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)

        #Check that the sale numbers are now available
        self.assertEqual(as_json[0]["purchaseCount"], 0)
        self.assertEqual(as_json[0]["name"], "test game")

        #"Buy" game
        game.purchaseCount = 1
        game.save(update_fields=["purchaseCount"])

        #Make GET request with correct headers
        response = client.get("/api/v1/salenumbers/", HTTP_AUTHORIZATION="Token " + str(token))
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)

        #Check that the sale numbers are available
        #and the purchase count is be updated
        self.assertEqual(as_json[0]["purchaseCount"], 1)
        self.assertEqual(as_json[0]["name"], "test game")
