from rest_framework import serializers
from gamedata.models import Game

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)

class DeveloperSerializer(serializers.Serializer):
    user = UserSerializer()

class PlayerSerializer(serializers.Serializer):
    user = UserSerializer()

'''
class GameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 100)
    price = serializers.FloatField()

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

    category = serializers.ChoiceField(choices = CATEGORIES)
    developer = DeveloperSerializer()
'''

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'name', 'price', 'category')


class HighscoreSerializer(serializers.Serializer):
    user = PlayerSerializer()
    highscore = serializers.IntegerField()
