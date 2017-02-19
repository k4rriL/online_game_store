from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

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

    CATEGORIES = (
        ('SPO', 'Sports'),
        ('RAC', 'Racing'),
        ('RPG', 'RPG'),
        ('ACT', 'Action'),
        ('ADV', 'Adventure'),
        ('CAS', 'Casual'),
        ('STR', 'Strategy'),
        ('OTH', 'Other')
    )

    category = models.CharField(max_length = 7, choices = CATEGORIES)
    class Meta:
        ordering = ("-purchaseCount",)

#Model 'extended' from user that represents a user that can buy games
class Player(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

#Model 'extended' from user that represents a user that can add games
class Developer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

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

#Function for creating authentication token for users
#automatically when new user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
