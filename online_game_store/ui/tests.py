from django.test import TestCase
from django.urls import reverse
from django.db import connection
from gamedata.models import Game, Player, Developer
from django.contrib.auth.models import User



class MainViewTests(TestCase):



    #Function for testing the game_info view
    def test_function_game_info(self):

        #Define some test data
        user = User.objects.create_user(username="testuseri", password="testpass")
        developer = Developer.objects.create(user=user)
        game = Game.objects.create(name="test game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")

        response = self.client.get("/game/1212")
        #Should return 404 with a invalid game id
        self.assertEqual(response.status_code, 404)

        response = self.client.get("/game/"+str(game.id))
        #Should return 200 with a valid game id
        self.assertEqual(response.status_code, 200)
