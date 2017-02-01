from django.shortcuts import render
from django.http import Http404, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from gamedata.models import Game, GamesOfPlayer
from gamedata.serializers import GameSerializer, HighscoreSerializer

def games_json(request, page = 1):
    categoryRequested = request.GET.get("category")
    search = request.GET.get("q")
    gamesPerPage= 20
    offset = int(request.GET.get('offset', 0))
    end = offset + gamesPerPage
    try:
        if categoryRequested is None and search is None:
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
    for i in p:
        c = {}
        c["name"] = i.name
        c["address"] = i.address
        c["price"] = i.price
        c["description"] = i.description
        c["id"] = i.id
        c["purchaseCount"] = i.purchaseCount
        c["developer"] = i.developer.user.email
        c["category"] = i.category
        games.append(c)
    data = json.dumps(games)

    if request.GET.get("callback") != None:
        data = '%s(%s);' % (request.GET.get("callback"),data)
        return HttpResponse(data, content_type="text/javascript")
    return HttpResponse(data, content_type="application/json")


class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def game_list(request):

    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return JSONResponse(serializer.data)

    return JSONResponse("[{}]")

@csrf_exempt
def game(request, gameid):

    games = Game.objects.filter(id=gameid)
    if games.count() > 0:
        game = Game.objects.get(id=gameid)
        serializer = GameSerializer(game)
        return JSONResponse(serializer.data)

    return JSONResponse("[{}]")


@csrf_exempt
def highscores(request, gameid):

    game = Game.objects.get(id=gameid)
    games = GamesOfPlayer.objects.filter(game=gameid)
    if games.count() > 0:
        serializer = HighscoreSerializer(games, many=True)
        return JSONResponse(serializer.data)
