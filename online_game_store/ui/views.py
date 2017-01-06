from django.shortcuts import render, get_object_or_404
from gamedata.models import Game
from hashlib import md5

# Create your views here.

def front(request):
    context = {}
    return render(request, "ui/index.html", context)


def game_info(request):
    context = {}
    #Test game
    game = get_object_or_404(Game, id=1234)
    context["game"] = game
    pid = game.name + game.developer.user.email
    sid = "lehtinj14"
    checksum = calculateHash(pid, sid, game.price, "36407fe6f70e3a4350d7535c28617aa6")
    context["checksum"] = checksum
    context["pid"] = pid
    context["sid"] = sid
    print(checksum)
    return render(request, "ui/showgame.html", context)


def game_purchase_success(request):

    if request.GET["result"] == "success":
        #TODO add specific game for game owner and update models


    #TODO update this to redirect to game
    return front(request)



def calculateHash(pid, sid, amount, token):
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, token)
    m = md5()
    m.update(checksumstr.encode("ascii"))
    return m.hexdigest()
