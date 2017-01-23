from django.shortcuts import render
from django.http import Http404, HttpResponse
import json

from .models import Game

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
            print(categoryRequested);
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
