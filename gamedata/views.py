from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from gamedata.serializers import GameSerializer, HighscoreSerializer, SaleSerializer
from .models import Game, Player, GamesOfPlayer, Developer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


"""
This view returns a list of games and information about them according to parameters:
List of optional parameters:
category: representing a category of games, e.g. Action
q: represents a search query, the function will return all games that contain the query-string
player: If only games owned by a certain player are wanted, the id of the user can be given as the value of this parameter
developer: If only games owned by a certain developer, the id of the user can be given as the value of this parameter
offset: if some games are already requested, you can use this parameter to get the next games

The games will be returned in JSON format.
"""
def games_json(request):
    categoryRequested = request.GET.get("category")
    search = request.GET.get("q")
    player = request.GET.get("player")
    developer = request.GET.get("developer")
    gamesPerPage = 20
    offset = int(request.GET.get("offset", 0))
    end = offset + gamesPerPage
    try:
        if player is not None and search is None:
            c = get_object_or_404(Player, user__id=int(player)).games.all()[offset:end]
            p = []
            for i in c:
                a = {}
                a["name"] = i.game.name
                a["address"] = i.game.address
                a["price"] = i.game.price
                a["description"] = i.game.description
                a["id"] = i.game.id
                a["category"] = i.game.get_category_display()
                p.append(a)
        elif player is not None and search is not None:
            c = get_object_or_404(Player, user__id=int(player)).games.filter(game__name__contains = search)[offset:end]
            p = []
            for i in c:
                if search in i.game.name:
                    a = {}
                    a["name"] = i.game.name
                    a["address"] = i.game.address
                    a["price"] = i.game.price
                    a["description"] = i.game.description
                    a["id"] = i.game.id
                    a["category"] = i.game.get_category_display()
                    p.append(a)
        elif developer is not None and search is None:
            c = get_object_or_404(Developer, user__id=int(developer))
            p = c.games.all()[offset:end]
        elif developer is not None and search is not None:
            p = get_object_or_404(Developer, user__id=int(developer)).games.filter(name__contains = search)[offset:end]
        elif categoryRequested is None and search is None:
            p = Game.objects.all()[offset:end]
        elif categoryRequested is not None and search is None:
            print(Game.categories_reverse[categoryRequested] + '')
            p = Game.objects.filter(category__exact = Game.categories_reverse[categoryRequested])[offset:end]
        elif categoryRequested is None and search is not None:
            p = Game.objects.filter(name__contains = search)[offset:end]
        else:
            p = Game.objects.filter(name__contains = search).filter(category__exact = Game.categories_reverse[categoryRequested])[offset:end]
    except Game.DoesNotExist:
        raise Http404("No games found")
    games = []

    '''
    Check whether data is already in dictionary or not and act accordingly.
    This check is necessary because we have to loop through GamesOfPlayer objects
    in above statements.
    '''
    if player is not None:
        data = json.dumps(p)
    else:
        for i in p:
            c = {}
            c["name"] = i.name
            c["address"] = i.address
            c["price"] = i.price
            c["description"] = i.description
            c["id"] = i.id
            c["category"] = i.get_category_display()
            games.append(c)
        data = json.dumps(games)

    #in case of JSONP
    if request.GET.get("callback") != None:
        data = '%s(%s);' % (request.GET.get("callback"), data)
        return HttpResponse(data, content_type = "text/javascript")
    return HttpResponse(data, content_type = "application/json")


'''
This function is used to get all available games
when request is made to API
'''
@csrf_exempt
def game_list(request):

    game_list = []
    games = Game.objects.all()
    for game in games:
        game_info = get_games_info(game)
        game_list.append(game_info)

    data = json.dumps(game_list)
    return HttpResponse(data, content_type = "application/json")


'''
Function for a case when specific game is
requested.
'''
@csrf_exempt
def game(request, gameid):

    games = Game.objects.filter(id = gameid)

    #Check that the game exists
    if games.count() > 0:
        game = Game.objects.get(id = gameid)
        game_info = get_games_info(game)
        return HttpResponse([game_info], content_type = "application/json")

    return HttpResponse("{}", content_type = "application/json")


'''
Function which returns highscores
of a specific game.
'''
@csrf_exempt
def highscores(request, gameid):

    game = Game.objects.filter(id=gameid)
    #Check that the game exists
    if game.count() > 0:

        game = Game.objects.get(id = gameid)
        games = GamesOfPlayer.objects.filter(game = gameid)
        #Check that the game has been bought so that
        #there are any highscores

        if games.count() > 0:
            games_list = []
            for game in games:
                info = {}
                info["user"] = game.user.user.username
                info["highscore"] = game.highscore
                games_list.append(info)
                return HttpResponse(games_list, content_type = "application/json")

    return HttpResponse("{}", content_type = "application/json")


'''
This function requires authentication token to
to access its methods. Token needs to be in the
headers of the GET request e.g.: Authorization: yourtokenhere
'''
def sales_numbers(request):

    token = None
    #Check that the token is given in the headers
    try:
        token = request.META["HTTP_AUTHORIZATION"]
    except KeyError:
        return HttpResponse("Remember to give the authorization token.", content_type="text/plain")

    if Developer.objects.filter(token=token).count() == 0:
        return HttpResponse("Invalid token.", content_type="text/plain")

    else:
        developer = Developer.objects.get(token=token)
        games = Game.objects.filter(developer = developer)
        games_list = []

        #Check that there are any games
        if games.count() > 0:
            for game in games:
                info = {}
                info["purchasecount"] = game.purchaseCount
                info["name"] = game.name
                games_list.append(info)

            data = json.dumps(games_list)
            return HttpResponse(data, content_type = "application/json")

    #Developer doesn't have games, return empty
    return HttpResponse("{}", content_type = "application/json")



#simple function for getting data
#from a game model
def get_games_info(game):
    info = {}
    info["price"] = game.price
    info["id"] = game.id
    info["name"] = game.name
    info["category"] = game.category
    return info
