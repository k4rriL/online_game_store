from django.shortcuts import render, get_object_or_404, redirect
from gamedata.models import Game, Player, GamesOfPlayer
from django.contrib.auth.models import User
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
    #Test user
    test_user = get_object_or_404(User, username="My Testuser")
    player = get_object_or_404(Player, user=test_user)
    context["player"] = player

    pid = str(game.id) + player.user.username.replace(" ", "")
    sid = "OnlineGameStore"
    token = "5fa6f9b7ea1628e4d373b4003bce9eb5"
    amount = game.price
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, token)
    checksum = calculateHash(checksumstr)
    context["checksum"] = checksum
    context["pid"] = pid
    context["sid"] = sid

    return render(request, "ui/showgame.html", context)


def game_purchase_success(request):

    context = {}
    pid = request.GET["pid"]
    game_id = request.GET["id"]
    ref = request.GET["ref"]
    result = request.GET["result"]
    checksum = request.GET["checksum"]
    game = get_object_or_404(Game, id=game_id)
    #Test user
    test_user = get_object_or_404(User, username="My Testuser")
    player = get_object_or_404(Player, user=test_user)
    secret_key = "5fa6f9b7ea1628e4d373b4003bce9eb5"
    checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
    correct_checksum = calculateHash(checksumstr)
    if request.GET["result"] == "success" and correct_checksum == checksum:
        new_relation = GamesOfPlayer.objects.create(game=game, user=player, highscore=0, gameState="Ready")
        new_relation.save()

    #TODO update this to redirect to game
    return front(request)


def calculateHash(str):
    m = md5()
    m.update(str.encode("ascii"))
    return m.hexdigest()
