from rest_framework import serializers
from gamedata.models import Game, GamesOfPlayer

#serializer to view all the available games
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'name', 'price', 'category')

#serializer to view the high scores for a game
class HighscoreSerializer(serializers.Serializer):
    user = serializers.ReadOnlyField(source="user.user.username")
    highscore = serializers.IntegerField()

    class Meta:
        model = GamesOfPlayer
        fields = ('user')

#serializer to view the sale numbers
class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('name', 'purchaseCount')
