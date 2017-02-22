from django.test import TestCase
from django.urls import reverse
from django.db import connection
from gamedata.models import Game, Player, Developer, GamesOfPlayer
from django.contrib.auth.models import User
from django.test import TransactionTestCase, Client
from . import views
from django.http import HttpResponseRedirect



class MainViewTests(TestCase):



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


    def test_game_purchase_success(self):


        #Define some test data
        user_for_dev = User.objects.create_user(username="testdev", password="testpass")
        user_for_player = User.objects.create_user(username="testplayer", password="testpass")
        developer = Developer.objects.create(user=user_for_dev)
        player = Player.objects.create(user=user_for_player)
        game = Game.objects.create(name="test game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")

        gameId=str(game.id)
        #correct checksum calculated from the parameters
        checksum = "97c5ef280e2f0f9be49e6275d1889c3f"
        client = Client()

        #Function requires login
        login = client.login(username="testplayer", password="testpass")
        #Should be able to login with correct credentials
        self.assertTrue(login)

        response = client.get("/games/success/?id=" + gameId + "&pid=" + gameId + "testplayer", follow=True)
        #Should redirect to home with invalid parameters
        self.assertEqual(response.redirect_chain, [("/", 302)])

        response = client.get("/games/success/?id=" + gameId + "&pid=" + gameId
                                                    + "testplayer&ref=1234", follow=True)
        #Should redirect to home with invalid parameters
        self.assertEqual(response.redirect_chain, [("/", 302)])

        response = client.get("/games/success/?id=" + gameId + "&pid=" + gameId
                                                    + "testplayer&ref=1234&result=success", follow=True)        #Should redirect to home with invalid parameters
        self.assertEqual(response.redirect_chain, [("/", 302)])

        response = client.get("/games/success/?id=" + gameId + "&pid=" + gameId
                                                    + "testplayer&ref=1234&result=success"
                                                    + "&checksum=" + checksum, follow=True)        #Should redirect to home with invalid parameters
        #Should redirect to the game with valid parameters
        self.assertEqual(response.redirect_chain, [("/game/" + gameId, 302)])

        #The game should have been added for the player
        self.assertTrue(GamesOfPlayer.objects.filter(user=player).count() == 1)

        #Test that the purchaseCount was updated
        self.assertTrue(Game.objects.get(id=gameId).purchaseCount == 1)


    def test_add_game(self):


        #Define some test data
        user_for_dev = User.objects.create_user(username="testdev", password="testpass")
        developer = Developer.objects.create(user=user_for_dev)
        game = Game.objects.create(name="test game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")

        client = Client()

        #Function requires login
        login = client.login(username="testdev", password="testpass")
        #Should be able to login with correct credentials
        self.assertTrue(login)

        response = client.post("/addnewgame/", {"name": "test"})
        #Should redirect to manage and not add the game with these invalid parameters
        self.assertEqual(response.url, "/manage")
        self.assertTrue(Game.objects.filter(name="test").count() == 0)

        response = client.post("/addnewgame/", {"name": "test", "url": "http://yle.fi"})
        #Should redirect to manage and not add the game with these invalid parameters
        self.assertEqual(response.url, "/manage")
        self.assertTrue(Game.objects.filter(name="test").count() == 0)

        response = client.post("/addnewgame/", {"name": "test", "url": "http://yle.fi",
                                                "description": "testing"})
        #Should redirect to manage and not add the game with these invalid parameters
        self.assertEqual(response.url, "/manage")
        self.assertTrue(Game.objects.filter(name="test").count() == 0)

        response = client.post("/addnewgame/", {"name": "test", "url": "http://yle.fi",
                                                "description": "testing", "price": 1.99 })
        #Should redirect to manage and not add the game with these invalid parameters
        self.assertEqual(response.url, "/manage")
        self.assertTrue(Game.objects.filter(name="test").count() == 0)

        response = client.post("/addnewgame/", {"name": "test", "url": "http://yle.fi",
                                               "description": "testing", "price": 1.99,
                                               "category": "Action" })
        #Should return to manage and add the game with correct parameters
        self.assertEqual(response.url, "/manage")
        self.assertTrue(Game.objects.filter(name="test").count() == 1)

        response = client.post("/addnewgame/", {"name": "test game", "url": "http://yle.fi",
                                               "description": "testing", "price": 1.99,
                                               "category": "Action" })
        #Should return to addnewgame and not add the new game because it has the same name
        #as the old game
        self.assertEqual(response.context[-1]["name_error"], "Sorry, this name is already in use")
        self.assertTrue(Game.objects.filter(name="test game").count() == 1)


    def test_delete_game(self):


        #Define some test data
        user_for_dev = User.objects.create_user(username="testdev", password="testpass")
        developer = Developer.objects.create(user=user_for_dev)
        game = Game.objects.create(name="test game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")

        client = Client()
        #Function requires login
        login = client.login(username="testdev", password="testpass")
        #Should be able to login with correct credentials
        self.assertTrue(login)

        response = client.post("/deletegame/")
        #Should only return redirect to manage and not crash without
        #the parameter gameid
        self.assertEqual(response.url, "/manage")

        response = client.post("/deletegame/", {"gameid": game.id})
        #Should redirect to manage and remove the wanted game
        self.assertEqual(response.url, "/manage")
        self.assertTrue(Game.objects.filter(id=game.id).count() == 0)


    def test_hasher(self):

        test_string = "teststring"
        correct = "d67c5cbf5b01c9f91932e3b8def5e5f8"
        #Hash the test string
        hashed = views.calculateHash(test_string)
        #Check that it is correct
        self.assertEqual(hashed, correct)


    def test_modify(self):

        #Define some test data
        user_for_dev = User.objects.create_user(username="testdev", password="testpass")
        user_for_dev2 = User.objects.create_user(username="testdev2", password="testpass")
        user_for_player = User.objects.create_user(username="testplayer", password="testpass")
        developer = Developer.objects.create(user=user_for_dev)
        developer2 = Developer.objects.create(user=user_for_dev2)
        player = Player.objects.create(user=user_for_player)
        game = Game.objects.create(name="test game", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")

        client = Client()
        #Function requires login
        login = client.login(username="testplayer", password="testpass")
        #Should be able to login with correct credentials
        self.assertTrue(login)

        response = client.get("/modify/" + str(game.id), follow=True)
        #Should only return redirect to main page
        #when trying to modify game with player
        self.assertEqual(response.redirect_chain, [("/", 302)])

        #login with developer who doesn't own this game
        login = client.login(username="testdev2", password="testpass")
        #Should be able to login with correct credentials
        self.assertTrue(login)

        response = client.get("/modify/1" + str(game.id), follow=True)
        #Should redirect to manage when trying to modify game with
        #invalid id
        self.assertEqual(response.redirect_chain, [("/manage/", 302)])

        response = client.get("/modify/" + str(game.id), follow=True)
        #Should return the manage view with developer who
        #doesn't own this specific game but is trying to modify it
        self.assertEqual(response.redirect_chain, [("/manage/", 302)])

        #login with developer who does own this game
        login = client.login(username="testdev", password="testpass")
        #Should be able to login with correct credentials
        self.assertTrue(login)

        response = client.get("/modify/" + str(game.id), follow=True)
        #Should return the modify view for this specific game
        #when the logged in developer is correct and set the
        #context correctly
        context = response.context[-1]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(context["game"], game)
        self.assertEqual(context["developerUser"], developer)
        self.assertEqual(context["highscores"], [])


    def test_modify_game(self):


        #Define some test data
        user_for_dev = User.objects.create_user(username="testdev", password="testpass")
        developer = Developer.objects.create(user=user_for_dev)
        game = Game.objects.create(name="test", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")
        game1 = Game.objects.create(name="test2", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")

        client = Client()

        #Function requires login
        login = client.login(username="testdev", password="testpass")
        #Should be able to login with correct credentials
        self.assertTrue(login)

        response = client.post("/modifygame/", {"name": "new name"})
        #Should redirect to manage and not modify the game with these invalid parameters
        self.assertEqual(response.url, "/manage/")
        self.assertTrue(Game.objects.filter(name="test").count() == 1)


        response = client.post("/modifygame/", {"name": "new name", "url": "http://yle.fi",
                                                "description": "testing", "price": 1.99})
        #Should redirect to manage and not modify the game with these invalid parameters
        self.assertEqual(response.url, "/manage/")
        self.assertTrue(Game.objects.filter(name="test").count() == 1)

        response = client.post("/modifygame/", {"name": "test3", "url": "http://yle.fi",
                                               "description": "testing", "price": 1.99,
                                               "category": "Action", "gameid": str(game.id)})
        #Should return to manage and modify the game with correct parameters
        self.assertEqual(response.url, "/manage/")
        self.assertEqual(Game.objects.filter(name="test").count(), 0)
        self.assertTrue(Game.objects.filter(name="test3").count() == 1)

        response = client.post("/modifygame/", {"name": "test2", "url": "http://yle.fi",
                                               "description": "testing", "price": 1.99,
                                               "category": "Action", "gameid": str(game.id)})
        #Should return to modifygame and not modify the name of
        #the game because it has the same name as this developer's
        #other game
        self.assertEqual(response.context[-1]["name_error"], "Sorry, this name is already in use")
        self.assertEqual(Game.objects.filter(name="test3").count(), 1)


    def test_get_highscores_and_game_for_context(self):

        #Define some test data
        user_for_dev = User.objects.create_user(username="testdev", password="testpass")
        developer = Developer.objects.create(user=user_for_dev)
        game = Game.objects.create(name="test", address="asdf@asdf.com", description="my test game", price=13.99, purchaseCount=0, developer=developer, category="SPO")

        context = {}
        context = views.get_highscores_and_game_for_context(context, game)
        self.assertEqual(context["highscores"], [])
        self.assertEqual(context["game"], game)
