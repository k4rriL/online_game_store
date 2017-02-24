from django.test import TestCase
from django.urls import reverse
from django.db import connection
from gamedata.models import Game, Player, Developer, GamesOfPlayer
from django.contrib.auth.models import User
from django.test import TransactionTestCase, Client
from . import views
from ui import views as views2
import json


class GameDataViewTests(TestCase):

    def test_games_json(self):

        client = Client()
        #Define some test data
        user_for_dev = User.objects.create_user(username="testdev", password="testpass")
        token = views2.calculate_token(user_for_dev)
        developer = Developer.objects.create(user=user_for_dev, token=token)
        user_for_player = User.objects.create_user(username="testplayer", password="testpass")
        player = Player.objects.create(user=user_for_player)
        user_for_dev2 = User.objects.create_user(username="testdev2", password="testpass")
        token = views2.calculate_token(user_for_dev2)
        developer2 = Developer.objects.create(user=user_for_dev2, token=token)

        game = Game.objects.create(name="Awesome game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="ACT")
        game2 = Game.objects.create(name="Test123", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer2, category="SPO")
        game3 = Game.objects.create(name="Adventure", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="ADV")
        game4 = Game.objects.create(name="Casual", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer2, category="CAS")

        playerPurchase1 = GamesOfPlayer.objects.create(game=game, user=player, highscore=0, gameState = "")
        playerPurchase2 = GamesOfPlayer.objects.create(game=game2, user=player, highscore=0, gameState = "")
        playerPurchase3 = GamesOfPlayer.objects.create(game=game4, user=player, highscore=0, gameState = "")

        #Check that the response contains correct
        #information about these two games
        response = client.get("/api/games/", **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)
        self.assertEqual(as_json[0]["id"], game.id)
        self.assertEqual(as_json[1]["id"], game2.id)

        #Check setting offset parameter
        response = client.get("/api/games/", {"offset":"1"}, **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)
        self.assertEqual(len(as_json), 3)
        self.assertEqual(as_json[0]["id"], game2.id)

        #Check if setting category parameter works
        response = client.get("/api/games/", {"category":"Sports"}, **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)
        self.assertEqual(len(as_json), 1)
        self.assertEqual(as_json[0]["id"], game2.id)

        #Check if setting query parameter works
        response = client.get("/api/games/", {"q":"Awe"}, **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)
        self.assertEqual(len(as_json), 1)
        self.assertEqual(as_json[0]["id"], game.id)

        #Check with another query
        response = client.get("/api/games/", {"q":"a"}, **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)
        self.assertEqual(len(as_json), 3)
        self.assertEqual(as_json[0]["id"], game.id)
        self.assertEqual(as_json[1]["id"], game3.id)
        self.assertEqual(as_json[2]["id"], game4.id)

        #Check category and query parameters together
        response = client.get("/api/games/", {"q":"a", "category":"Casual"}, **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)
        self.assertEqual(len(as_json), 1)
        self.assertEqual(as_json[0]["id"], game4.id)

        #Check setting developer parameter
        response = client.get("/api/games/", {"developer":user_for_dev.id}, **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)
        self.assertEqual(len(as_json), 2)
        self.assertEqual(as_json[0]["id"], game.id)
        self.assertEqual(as_json[1]["id"], game3.id)

        #Check setting developer parameter and query
        response = client.get("/api/games/", {"developer":user_for_dev.id, "q":"Adven"}, **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)
        self.assertEqual(len(as_json), 1)
        self.assertEqual(as_json[0]["id"], game3.id)

        #Check setting player parameter
        response = client.get("/api/games/", {"player":user_for_player.id}, **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)
        self.assertEqual(len(as_json), 3)
        self.assertEqual(as_json[0]["id"], game.id)
        self.assertEqual(as_json[1]["id"], game2.id)
        self.assertEqual(as_json[2]["id"], game4.id)

        #Check setting player parameter and query
        response = client.get("/api/games/", {"player":user_for_player.id, "q":"Test"}, **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)
        self.assertEqual(len(as_json), 1)
        self.assertEqual(as_json[0]["id"], game2.id)

    def test_game_list(self):

        #Define some test data
        user_for_dev = User.objects.create_user(username="testdev", password="testpass")
        developer = Developer.objects.create(user=user_for_dev)
        game = Game.objects.create(name="test game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")
        game2 = Game.objects.create(name="test2 game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")

        client = Client()
        #Check that the response contains correct
        #information about these two games
        response = client.get("/api/v1/games/", **{'wsgi.url_scheme': 'https'})
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
        token = views2.calculate_token(user_for_dev)
        developer = Developer.objects.create(user=user_for_dev, token=token)
        game = Game.objects.create(name="test game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")

        client = Client()
        #Check that the response contains correct
        #information about these two games
        response = client.get("/api/v1/games/" + str(game.id), **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")

        #Check that the response contains correct
        #information about this game
        self.assertTrue(game.name in content)
        self.assertTrue(str(game.id) in content)
        self.assertTrue(str(game.price) in content)
        self.assertTrue(game.category in content)

        response = client.get("/api/v1/games/1" + str(game.id), **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)

        #Check that with a wrong id, the response is empty
        self.assertEqual(as_json, {})



    def test_highscores(self):

        #Define some test data
        user_for_dev = User.objects.create_user(username="testdev", password="testpass")
        user_for_player = User.objects.create_user(username="testplayer", password="testpass")
        token = views2.calculate_token(user_for_dev)
        developer = Developer.objects.create(user=user_for_dev, token=token)
        player = Player.objects.create(user=user_for_player)
        game = Game.objects.create(name="test game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")
        game_of_player = GamesOfPlayer.objects.create(game=game, user=player, highscore="100", gameState="assdf")

        #Create client and make GET request
        client = Client()
        response = client.get("/api/v1/highscores/" + str(game.id), **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")

        #Check that the response contains correct
        #information about this game's highscores
        self.assertTrue(player.user.username in content)
        self.assertTrue("100" in content)
        '''
        self.assertEqual(as_json[0]["user"], "testplayer")
        self.assertEqual(as_json[0]["highscore"], 100)
        '''

        #Check that response is correct with invalid game id
        response = client.get("/api/v1/highscores/1" + str(game.id), **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")
        as_json = json.loads(content)

        #Check that the response contains correct
        #information about this game
        self.assertEqual(as_json, {})



    def test_salenumbers(self):

        #Define some test data
        user_for_dev = User.objects.create_user(username="testdev", password="testpass")
        user_for_player = User.objects.create_user(username="testplayer", password="testpass")
        token = views2.calculate_token(user_for_dev)
        developer = Developer.objects.create(user=user_for_dev, token=token)
        player = Player.objects.create(user=user_for_player)
        game = Game.objects.create(name="test game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")

        #Create client and make GET request
        client = Client()
        response = client.get("/api/v1/salenumbers/", **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")

        #Check that the sale numbers are unavailable if
        #correct HTTP headers are not given
        self.assertEqual(content, "Remember to give the authorization token.")

        #Make GET request with correct headers
        response = client.get("/api/v1/salenumbers/", HTTP_AUTHORIZATION=token, **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")

        #Check that the sale numbers are now available

        self.assertTrue("purchasecount" in content)
        self.assertTrue("name" in content)

        #"Buy" game
        game.purchaseCount = 1
        game.save(update_fields=["purchaseCount"])

        #Make GET request with correct headers
        response = client.get("/api/v1/salenumbers/", HTTP_AUTHORIZATION=token, **{'wsgi.url_scheme': 'https'})
        content = response.content.decode("UTF-8")

        #Check that the sale numbers are available
        #and the purchase count is be updated
        self.assertTrue("purchasecount" in content)
        self.assertTrue("name" in content)
        self.assertTrue("1" in content)
