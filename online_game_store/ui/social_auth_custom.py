from gamedata.models import Player
from django.db import IntegrityError
from social_core.exceptions import AuthFailed

def addUserToPlayers(backend, user, response, *args, **kwargs):
    if user == None:
        # this should never happen, but the auth system should know better
        # what to do here
        return
    # Users logged in with external authentication are always put as players
    if Player.objects.filter(user=user).exists():
        # ok, the user has loggen in before
        return
    try:
        p = Player(user=user)
        p.save()
    except IntegrityError:
        # something is broken, cancel authentication
        raise AuthFailed
