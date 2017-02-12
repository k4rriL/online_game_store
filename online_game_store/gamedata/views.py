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
    offset = int(request.GET.get('offset', 0))
    end = offset + gamesPerPage
    try:
        if player is not None and search is None:
            c = get_object_or_404(Player, user__id=int(player)).games.all()
            p = []
            for i in c:
                a = {}
                a["name"] = i.game.name
                a["address"] = i.game.address
                a["price"] = i.game.price
                a["description"] = i.game.description
                a["id"] = i.game.id
                a["category"] = i.game.category
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
                    a["category"] = i.game.category
                    p.append(a)
        elif developer is not None and search is None:
            c = get_object_or_404(Developer, user__id=int(developer))
            p = c.games.all()[offset:end]
        elif developer is not None and search is not None:
            p = get_object_or_404(Developer, user__id=int(developer)).games.filter(name__contains = search)[offset:end]
        elif categoryRequested is None and search is None:
            p = Game.objects.all()[offset:end]
        elif categoryRequested is not None and search is None:
            p = Game.objects.filter(category__exact = categoryRequested)[offset:end]
        elif categoryRequested is None and search is not None:
            p = Game.objects.filter(name__contains = search)[offset:end]
        else:
            p = Game.objects.filter(name__contains = search).filter(category__exact = categoryRequested)[offset:end]
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
            print(i)
            c = {}
            c["name"] = i.name
            c["address"] = i.address
            c["price"] = i.price
            c["description"] = i.description
            c["id"] = i.id
            c["category"] = i.category
            games.append(c)
        data = json.dumps(games)

    #in case of JSONP
    if request.GET.get("callback") != None:
        data = '%s(%s);' % (request.GET.get("callback"), data)
        return HttpResponse(data, content_type = "text/javascript")
    return HttpResponse(data, content_type = "application/json")


#class for returning JSONResponse
class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

'''
This function is used to get all available games
when request is made to API
Creates new serializer from all available games
and returns JSONResponse
'''
@csrf_exempt
def game_list(request):

    games = Game.objects.all()
    serializer = GameSerializer(games, many = True)
    return JSONResponse(serializer.data)

    return JSONResponse("[{}]")


'''
Function for a case when specific game is
requested. Returns wanted game as JSONResponse
'''
@csrf_exempt
def game(request, gameid):

    games = Game.objects.filter(id = gameid)

    #Check that the game exists
    if games.count() > 0:
        game = Game.objects.get(id = gameid)
        serializer = GameSerializer(game)
        return JSONResponse(serializer.data)

    return JSONResponse("{}")


'''
Function which returns highscores
of a specific game. Returns highscores as JSONResponse
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
            serializer = HighscoreSerializer(games, many = True)
            return JSONResponse(serializer.data)

    return JSONResponse("[]")


'''
This class requires authentication token to
to access its methods. Token needs to be in the
headers of the GET request e.g.: Authorization: Token yourtokenhere
'''
class AuthView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    #returns highscores for authenticated developers
    def get(self, request):

        developer = get_object_or_404(Developer, user = request.user)
        games = Game.objects.filter(developer = developer)

        #Check that there are any games
        if games.count() > 0:
            serializer = SaleSerializer(games, many = True)
            return JSONResponse(serializer.data)

        #Case developer doesn't have any games return empty
        return JSONResponse("[]")
