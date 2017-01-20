from django.shortcuts import render, get_object_or_404, redirect
from gamedata.models import Game, Player, GamesOfPlayer
from django.contrib.auth.models import User
from hashlib import md5

# Create your views here.

def front(request):
    context = {}
    return render(request, "ui/index.html", context)


def category(request, category):
    context = {"category":category}
    return render(request, "ui/index.html", context)

def game_info(request, gameId):
    context = {}
    #Test game
    game = get_object_or_404(Game, id=gameId)
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

def add_new_game(request):

    #test user, TODO use authenticated developer
    test_user = get_object_or_404(User, username="testidevaaja")
    developer = Developer.objects.get(user=test_user)
    context = {}

    #Check if method is post
    if request.method == "POST":

        form = forms.NewGameForm(request.POST)
        if form.is_valid():

            name = request.POST["name"]
            url = request.POST["url"]
            description = request.POST["description"]
            price = float(request.POST["price"])
            id = int(time.time())

            #Check that there are no games with same id and name
            if Game.objects.filter(name=name).count() == 0 and  Game.objects.filter(id=id).count() == 0:
                new_game = Game.objects.create(id=id, name=name, address=url, description=description, price=price, purchaseCount=0, developer=developer)
                new_game.save()

            #Check that atleast the name is unique
            elif Game.objects.filter(name=name).count() == 0:
                id = int(str(randint(0, 10000)) + str(id))
                new_game = Game.objects.create(id=id, name=name, address=url, description=description, price=price, purchaseCount=0, developer=developer)
                new_game.save()

            #Else return to the form filled with old parameters
            else:
                context["name"] = name
                context["url"] = url
                context["description"] = description
                context["price"] = price
                context["name_error"] = "Sorry, this name is already in use"
                return render(request, "ui/addgame.html", context)

    #if the request method wasn't post, return the form view
    else:
        return render(request, "ui/addgame.html", context)

    #TODO maybe return the page of developer's games
    #now also including the newly added game?
    return render(request, "ui/index.html", context)

def calculateHash(str):
    m = md5()
    m.update(str.encode("ascii"))
    return m.hexdigest()
