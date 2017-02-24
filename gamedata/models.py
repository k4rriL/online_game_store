from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import URLValidator


class URLFieldForHTTPS(models.URLField):
  '''URL field that accepts URLs that start with https:// only.'''
  default_validators = [URLValidator(schemes=['https'])]

'''
This model represents a single game
developer field is a reference to Developer object
'''
class Game(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    address = models.URLField()
    description = models.TextField()
    price = models.FloatField()
    purchaseCount = models.PositiveIntegerField()
    developer = models.ForeignKey('Developer', related_name='games')
    ACTION = 'ACT'
    ADVENTURE = 'ADV'
    CASUAL = 'CAS'
    RACING = 'RAC'
    RPG = 'RPG'
    SPORTS = 'SPO'
    STRATEGY = 'STR'
    OTHER = 'OTH'


    CATEGORIES = (
        (ACTION, 'Action'),
        (ADVENTURE, 'Adventure'),
        (CASUAL, 'Casual'),
        (RACING, 'Racing'),
        (RPG, 'RPG'),
        (SPORTS, 'Sports'),
        (STRATEGY, 'Strategy'),
        (OTHER, 'Other')
    )

    categories_reverse = dict((v, k) for k, v in CATEGORIES)

    category = models.CharField(max_length = 3, choices = CATEGORIES, default=ACTION,)
    class Meta:
        ordering = ("-purchaseCount",)


#Model 'extended' from user that represents a user that can buy games
class Player(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

#Model 'extended' from user that represents a user that can add games
class Developer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    token = models.CharField(max_length=32, primary_key=True)

#Model that represents a single game of a player (contains highscore etc. data)
class GamesOfPlayer(models.Model):
    game = models.ForeignKey('Game')
    user = models.ForeignKey('Player', related_name = 'games')
    highscore = models.PositiveIntegerField()
    gameState = models.TextField()
    purchaseTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-highscore",)

#Model for storing email verification tokens
class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, unique=True)
    token = models.CharField(max_length = 32)
