from django.test import TestCase
from django.urls import reverse
from django.db import connection
from gamedata.models import Game, Player, Developer, GamesOfPlayer
from django.contrib.auth.models import User
from django.test import TransactionTestCase, Client
from . import views



class MainViewTests(TestCase):


    #Function for testing the game_info view
    def test_function_game_info(self):

        #Define some test data
        user_for_dev = User.objects.create_user(username="testdev", password="testpass")
        user_for_player = User.objects.create_user(username="testplayer", password="testpass")
        developer = Developer.objects.create(user=user_for_dev)
        player = Player.objects.create(user=user_for_player)
        game = Game.objects.create(name="test game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")
        client = Client()

        #First test with developer
        login = client.login(username="testdev", password="testpass")
        #Should be able to login with correct credentials
        self.assertTrue(login)

        response = client.get("/game/1212")
        #Should return 404 with a invalid game id
        self.assertEqual(response.status_code, 404)

        response = client.get("/game/"+str(game.id))
        #Should return 200 with a valid game id
        self.assertEqual(response.status_code, 200)

        context = response.context[-1]
        #Check that the context is set correctly for this developer
        self.assertEqual(context['owned'], False)
        self.assertEqual(context['playerUser'], None)
        self.assertEqual(context['developerUser'], developer)
        self.assertEqual(context['highscores'], [])
        self.assertEqual(context['game'], game)

        #context should not have these attributes since developer is logged in
        self.assertFalse("sid" in context)
        self.assertFalse("pid" in context)
        self.assertFalse("checksum" in context)

        #Now test with a player
        login = client.login(username="testplayer", password="testpass")
        self.assertTrue(login)

        response = client.get("/game/1212")
        #Should return 404 with a invalid game id
        self.assertEqual(response.status_code, 404)

        response = client.get("/game/"+str(game.id))
        #Should return 200 with a valid game id
        self.assertEqual(response.status_code, 200)

        context = response.context[-1]
        #Check that the context is set correctly for this player
        self.assertEqual(context['owned'], False)
        self.assertEqual(context['playerUser'], player)
        self.assertEqual(context['developerUser'], None)
        self.assertEqual(context['highscores'], [])
        self.assertEqual(context['game'], game)

        pid = str(game.id) + "testplayer"
        sid = "OnlineGameStore"
        checksum = "a6b00b196fd189729d33c565c61f486e"

        #Now the context should also have this attributes and check that they are correct
        self.assertEqual(context['pid'], pid)
        self.assertEqual(context['sid'], sid)
        self.assertEqual(context['checksum'], checksum)

        #Add this game for the player
        game_of_player = GamesOfPlayer.objects.create(game=game, user=player, highscore="100", gameState="assdf")

        #get the game_info view again now that the player has this game
        response = client.get("/game/"+str(game.id))
        self.assertEqual(response.status_code, 200)

        context = response.context[-1]
        #Check that the attributes have changed
        self.assertEqual(context['owned'], True)
        self.assertEqual(context['highscores'][0]['score'], 100)


    def test_hasher(self):

        test_string = "teststring"
        correct = "d67c5cbf5b01c9f91932e3b8def5e5f8"
        #Hash the test string
        hashed = views.calculateHash(test_string)
        #Check that it is correct
        self.assertEqual(hashed, correct)
