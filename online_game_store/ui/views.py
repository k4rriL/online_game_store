from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from gamedata.models import Game, Player, GamesOfPlayer, Developer, EmailVerificationToken
from django.contrib.auth.models import User
from hashlib import md5
from django.http import *
from random import randint, choice
from django.db.models import F
from django.db import DatabaseError, transaction
import time
from . import forms
from rest_framework.authtoken.models import Token
from ui.forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
import string
import django.urls
from django.contrib.staticfiles.templatetags.staticfiles import static

#Returns the front page of the website
def front(request):
    context = {}
    developerUser = None
    playerUser = None
    if request.user.is_authenticated():
        try:
            playerUser = Player.objects.get(user=request.user)
        except Player.DoesNotExist:
            print("player does not exist")
        try:
            developerUser = Developer.objects.get(user=request.user)
        except Developer.DoesNotExist:
            print("Developer does not exist")
    context["playerUser"] = playerUser
    context["developerUser"] = developerUser
    return render(request, "ui/index.html", context)

#Returns a category page, category is defined by the parameter
def category(request, category):
    context = {"category":category}
    developerUser = None
    playerUser = None
    if request.user.is_authenticated():
        try:
            playerUser = Player.objects.get(user=request.user)
        except Player.DoesNotExist:
            print("player does not exist")
        try:
            developerUser = Developer.objects.get(user=request.user)
        except Developer.DoesNotExist:
            print("developer does not exist")
    context["playerUser"] = playerUser
    context["developerUser"] = developerUser
    return render(request, "ui/index.html", context)

'''
Returns the view where user has clicked a game.
Displays info of the chosen game and possibly
creates form for purchasing this game.
'''
def game_info(request, gameId):
    context = {}
    game = get_object_or_404(Game, id=gameId)
    context["game"] = game
    developerUser = None
    playerUser = None
    owned = False
    #Check that the user is authenticated
    if request.user.is_authenticated():

        try:
            playerUser = Player.objects.get(user=request.user)
        except Player.DoesNotExist:
            print("player does not exist")

        try:
            developerUser = Developer.objects.get(user=request.user)
        except Developer.DoesNotExist:
            print("developer does not exist")

        if playerUser is not None:

            player = playerUser
            context["player"] = player
            playersGames = GamesOfPlayer.objects.filter(user=player)

            for i in playersGames:
                if i.game.id == game.id:
                    owned = True

            #Define some parameters for the form
            pid = str(game.id) + player.user.username.replace(" ", "")
            sid = "OnlineGameStore"
            token = "5fa6f9b7ea1628e4d373b4003bce9eb5"
            amount = game.price

            checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, token)
            #Calculate the checksum for the form which can be posted to the payment system
            checksum = calculateHash(checksumstr)

            context["checksum"] = checksum
            context["pid"] = pid
            context["sid"] = sid
    context["owned"] = owned
    context["playerUser"] = playerUser
    context["developerUser"] = developerUser

    #Get highscores of a game to display them next to the game
    boughtGames = GamesOfPlayer.objects.filter(game=game)
    highscores = []

    for i in boughtGames:
        c = {}
        c["score"] = i.highscore
        c["name"] = i.user.user.username
        highscores.append(c)

    context["highscores"] = highscores

    gamePath = django.urls.reverse(game_info, kwargs={"gameId":gameId})
    gameUrl = request.build_absolute_uri(gamePath)
    context["gameUrl"] = gameUrl

    imgPath = static(game.category + ".jpg")
    imgUrl = request.build_absolute_uri(imgPath)
    context["imgUrl"] = imgUrl
    return render(request, "ui/showgame.html", context)

'''
Provide backend functionality for game-service interaction
'''
def game_interaction(request, gameId):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    game = get_object_or_404(Game, id=gameId)
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    player = None
    try:
        player = Player.objects.get(user=request.user)
    except Player.DoesNotExist:
        return HttpResponseForbidden()
    boughtGame = None
    try:
        boughtGame = GamesOfPlayer.objects.get(game=game, user=player)
    except GamesOfPlayer.DoesNotExist:
        # player doesn't own the game
        return HttpResponseForbidden()
    except MultipleObjectsReturned:
        # this should never happen
        return HttpResponseServerError()

    messageType = None
    try:
        messageType = request.POST['messageType']
    except KeyError:
        return HttpResponseBadRequest()

    if messageType == "SCORE":
        try:
            score = float(request.POST['score'])
        except KeyError:
            return HttpResponseBadRequest()
        if score > boughtGame.highscore:
            boughtGame.highscore = score
            boughtGame.save()
    elif messageType == "SAVE":
        try:
            gameState = request.POST['gameState']
        except KeyError:
            return HttpResponseBadRequest()
        boughtGame.gameState = gameState
        boughtGame.save()
    elif messageType == "LOAD_REQUEST":
        response = {}
        response["messageType"] = "LOAD"
        response["gameState"] = boughtGame.gameState
        return JsonResponse(response)
    else:
        return HttpResponseBadRequest()

    return HttpResponse("")

'''
Function for checking that the payment
was successful. User has to be logged in
in order to make a successful payment. This
function also adds this newly bought game to player's
collection by creating a new entry of model GamesOfPlayer
according to request.
'''
@login_required
def game_purchase_success(request):

    #Check that the request has correct parameters
    form = forms.SuccessfulPaymentForm(request.GET)
    if form.is_valid():

        #Get necessary parameters from request
        pid = request.GET["pid"]
        game_id = request.GET["id"]
        ref = request.GET["ref"]
        result = request.GET["result"]
        checksum = request.GET["checksum"]
        secret_key = "5fa6f9b7ea1628e4d373b4003bce9eb5"

        game = get_object_or_404(Game, id=game_id)
        player = get_object_or_404(Player, user=request.user)

        checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
        #calculate the checksum
        correct_checksum = calculateHash(checksumstr)

        '''
        Check that the payment was successful according to the
        payment service and that the checksum is correct
        '''
        if result == "success" and correct_checksum == checksum:
            #Create new entry
            new_relation = GamesOfPlayer.objects.create(game=game, user=player, highscore=0, gameState="Ready")
            new_relation.save()
            Game.objects.filter(id=game_id).update(purchaseCount=F("purchaseCount") + 1)
            #Redirect player to the game
            return HttpResponseRedirect("/game/"+ game_id)

    #In case of unsuccessful purchase, redirect
    #to home page
    return HttpResponseRedirect("/")


'''
Function for adding new game to the database. This
function is used when developers want to add their
game to the store. Creates new entry to the model
Game and checks that there is no game with the same name
'''
@login_required
def add_new_game(request):
    developer = Developer.objects.get(user=request.user)
    context = {}

    #Check if method is post
    if request.method == "POST":

        #validate the posted form
        form = forms.AddGameForm(request.POST)
        if form.is_valid():
		
            #Get infromation from the post request
            name = request.POST["name"]
            url = request.POST["url"]
            description = request.POST["description"]
            price = float(request.POST["price"])
            category = request.POST["category"]
			category3 = ""
			if category is "Sports":
				category3 = "SPO"
			elif category is "Racing":
				category3 = "RAC"
			elif category is "RPG":
				category3 = "RPG"
			elif category is "Action":
				category3 = "ACT"
			elif category is "Adventure":
				category3 = "ADV"
			elif category is "Casual":
				category3 = "CAS"
			elif category is "Strategy":
				category3 = "STR"
			else:
				category3 = "OTH"

            #Check that there are no games with same id and name
            if Game.objects.filter(name=name).count() == 0:
                new_game = Game.objects.create(name=name, address=url, description=description, price=price, purchaseCount=0, developer=developer, category=category3)
                new_game.save()

            #Else there is already a game with a same name
            #--> return the form filled with old parameters
            else:
                context["name"] = name
                context["url"] = url
                context["description"] = description
                context["price"] = price
                context["name_error"] = "Sorry, this name is already in use"
                return render(request, "ui/addgame.html", context)

        else:
            print("failed to validate")

    #if the request method wasn't post, return the form view
    else:
        return render(request, "ui/addgame.html", context)

    return HttpResponseRedirect("/manage")

'''
View for viewing game's information, modifying
this information(e.g. name, price...) and displaying
the highscores of a game
'''
@login_required
def modify(request, gameId):
    context = {}
    playerUser = None
    developerUser = None

    #Requires an authenticated user
    if request.user.is_authenticated():

        try:
            playerUser = Player.objects.get(user=request.user)
        except Player.DoesNotExist:
            print("player does not exist")

        try:
            developerUser = Developer.objects.get(user=request.user)
        except Developer.DoesNotExist:
            print("developer does not exist")

    context["playerUser"] = playerUser
    context["developerUser"] = developerUser

    #The user has to be a developer
    if playerUser is not None:
        return HttpResponseRedirect("/")

    #check that the game exists and that
    #logged in developer owns it
    game = Game.objects.filter(id=gameId).filter(developer=developerUser)
    if game.count() > 0:

        '''
        game = Game.objects.get(id=gameId)
        games = GamesOfPlayer.objects.filter(game=game)
        highscores = []

        #Get the highscores of a game so that they can be displayed
        #in the same view.
        for i in games:
            c = {}
            c["score"] = i.highscore
            c["name"] = i.user.user.first_name
            highscores.append(c)

        context["highscores"] = highscores
        context["game"] =  game
        context["games"] = games
        '''
        game = Game.objects.get(id=gameId)
        context = get_highscores_and_game_for_context(context, game)
        context["name"] = game.name

        return render(request, "ui/modifygame.html", context)

    return HttpResponseRedirect("/manage/")


'''
This function handles requests to modify a game.
When developer wants to modify his game's information,
this function is called to perform the modifications.
'''
@login_required
def modify_game(request):

    if request.method == "POST":

        #Validate the posted form
        form = forms.ModifyGameForm(request.POST)
        if form.is_valid():

            #Get the game and check that it exists
            #Also check that the game is really developed
            #by the logged in developer
            gameId = request.POST["gameid"]
            developer = get_object_or_404(Developer, user=request.user)
            game = Game.objects.filter(id=gameId).filter(developer=developer)
            if game.count() > 0:

                #Get information from the post request
                #and update game's fields according to the request
                game = Game.objects.get(id=gameId)
                description = request.POST["description"]
                price = request.POST["price"]
                name = request.POST["name"]
                category = request.POST["category"]
                address = request.POST["url"]

                nameCount = Game.objects.filter(name=name).count()
                game.description = description
                game.price = price
                game.category = category
                game.address = address

                #Check that if the developer changed the name
                #or there is no game that has the same name
                #as the new name
                if name == game.name or nameCount == 0:
                    game.name = name
                    game.save(update_fields=["description", "price", "name", "category", "address"])

                #Else return to the modifygame view and set the
                #context right
                else:
                    game.save(update_fields=["description", "price", "category", "address"])
                    context = {}
                    context = get_highscores_and_game_for_context(context, game)
                    context["name_error"] = "Sorry, this name is already in use"
                    return render(request, "ui/modifygame.html", context)

    return HttpResponseRedirect("/manage/")

'''
Function so that the developers can
also delete their games.
'''
@login_required
def delete_game(request):

    if request.method == "POST" and "gameid" in request.POST:

        #Check that the game exists
        gameId = request.POST["gameid"]
        if Game.objects.filter(id=gameId).count() > 0:
            game = Game.objects.get(id=gameId)
            game.delete()

    return HttpResponseRedirect("/manage")


#Returns view with all games owned by a certain user
@login_required
def your_games(request):
    context = {}
    developerUser = None
    playerUser = None
    if request.user.is_authenticated():
        try:
            playerUser = Player.objects.get(user=request.user)
        except Player.DoesNotExist:
            print("player does not exist")
        try:
            developerUser = Developer.objects.get(user=request.user)
        except Developer.DoesNotExist:
            print("developer does not exist")
    context["playerUser"] = playerUser
    context["developerUser"] = developerUser
    if developerUser is not None:
        return HttpResponseRedirect("/")
    player = get_object_or_404(Player, user=request.user)
    context["player"] = player
    return render(request, "ui/index.html", context)

#Returns view with all games added to store by a certain developer
@login_required
def manage(request):
    context = {}
    developerUser = None
    playerUser = None
    if request.user.is_authenticated():
        try:
            playerUser = Player.objects.get(user=request.user)
        except Player.DoesNotExist:
            print("player does not exist")
        try:
            developerUser = Developer.objects.get(user=request.user)
        except Developer.DoesNotExist:
            print("developer does not exist")
    context["playerUser"] = playerUser
    context["developerUser"] = developerUser
    if playerUser is not None:
        return HttpResponseRedirect("/")
    developer = get_object_or_404(Developer, user=request.user)
    p = developer.games.all()
    sum = 0
    for i in p:
        sum = sum + i.purchaseCount
    token = get_object_or_404(Token, user=request.user)
    context["token"] = token
    context["developer"] = developer
    context["sum"] = sum
    return render(request, "ui/index.html", context)

#Simple md5 hash function
def calculateHash(str):
    m = md5()
    m.update(str.encode("ascii"))
    return m.hexdigest()


'''
function for updating relevant information
to the context, used when displaying the
manage view. Returns the updated context
'''
def get_highscores_and_game_for_context(context, game):

    games = GamesOfPlayer.objects.filter(game=game)
    highscores = []

    #Get the highscores of a game so that they can be displayed
    #in the same view.
    for i in games:
        c = {}
        c["score"] = i.highscore
        c["name"] = i.user.user.first_name
        highscores.append(c)

    context["highscores"] = highscores
    context["game"] =  game
    context["games"] = games

    return context

#email verification confirmation
def verifyemail(request, userId, token):
    try:
        v = EmailVerificationToken.objects.get(user=userId, token=token)
    except EmailVerificationToken.DoesNotExist:
        return HttpResponseBadRequest()
    try:
        u = User.objects.get(pk=userId)
    except User.DoesNotExist:
        return HttpResponseBadRequest()
    u.is_active = True
    u.save()
    v.delete()
    return render(request, "ui/message.html", {"message": "Email verification successfull, now log in" })

#register new user to site
def register(request):
    context = {}
    if request.method == "POST": # try to add the user
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            try:
                # start transaction
                with transaction.atomic():
                    user = register_form.save()
                    # disable user until email is verified
                    user.is_active = False
                    user.save()
                    if register_form.cleaned_data['usertype'] == 'developer':
                        usertype = Developer(user=user)
                    else:
                        usertype = Player(user=user)
                    usertype.save()
                    # generate email verification
                    token = ''.join(choice(string.ascii_letters + string.digits) for i in range(32))
                    EmailVerificationToken(user=user, token=token).save()
                    path = django.urls.reverse(verifyemail, kwargs={"userId": str(user.pk), "token":token})
                    targetUrl = request.scheme + "://" + request.get_host() + path
                    hostname = request.get_host().split(":")[0]
                    send_mail(
                        'Online Game Store Email verification',
                        'Click on the following link to verify your email to the service ' +
                            '<a href="' + targetUrl + '">' + targetUrl + '</a>',
                        'noreply@'+hostname,
                        [user.email],
                        fail_silently=False,
                    )

                    # end of transaction, errors can be simulated with:
                    # raise DatabaseError
            except DatabaseError:
                register_form.add_error(None, "Database error, please try again")
                context["form"] = register_form
                return render(request, "registration/register.html", context)
            return render(request, "ui/message.html", {"message": "Email verification was sent to " + user.email })
    else: # show empty form
        register_form = RegisterForm()
    context["form"] = register_form
    return render(request, "registration/register.html", context)
