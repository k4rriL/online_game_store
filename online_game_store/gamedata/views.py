from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
import json

from .models import Game, Player, GamesOfPlayer, Developer

def games_json(request, page = 1):
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
                a["purchaseCount"] = i.game.purchaseCount
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
                    a["purchaseCount"] = i.game.purchaseCount
                    a["category"] = i.game.category
                    p.append(a)
        elif developer is not None and search is None:
            c = get_object_or_404(Developer, user__id=int(developer))
            print(c.games)
            p = c.games.all()[offset:end]
            print("as" + str(p.count()))
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
        print("derps")
        raise Http404("No games found")
    games = []
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
            c["purchaseCount"] = i.purchaseCount
            c["category"] = i.category
            games.append(c)
        data = json.dumps(games)

    if request.GET.get("callback") != None:
        data = '%s(%s);' % (request.GET.get("callback"),data)
        return HttpResponse(data, content_type="text/javascript")
    return HttpResponse(data, content_type="application/json")
