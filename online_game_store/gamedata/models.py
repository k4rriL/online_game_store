from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
    id = models.PositiveIntegerField(unique = True, primary_key = True)
    name = models.CharField(max_length = 100, unique = True)
    address = models.URLField()
    description = models.TextField()
    price = models.FloatField()
    purchaseCount = models.PositiveIntegerField()
    developerEmail = models.ForeignKey('Developer', related_name='games')

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

    category = models.CharField(max_length = 3, choices = CATEGORIES)
    class Meta:
        ordering = ("purchaseCount",)

class Player(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

class Developer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

class GamesOfPlayer(models.Model):
    gameID = models.ForeignKey('Game')
    username = models.ForeignKey('Player', related_name = 'games')
    highscore = models.PositiveIntegerField()
    gameState = models.TextField()