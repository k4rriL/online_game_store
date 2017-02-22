from django import forms
from django.forms import ModelForm
from gamedata.models import Game, URLFieldForHTTPS
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#Form for registering new users
class RegisterForm(UserCreationForm):
    typelist = [('player', 'Player'), ('developer', 'Developer')]
    usertype = forms.ChoiceField(choices=typelist, widget=forms.RadioSelect(), initial='player', help_text='Players can only play, developers only upload games.', label="User type")

    class Meta:
        model = User
        fields = ('username', 'email')

#Form for adding a new game
class AddGameForm(forms.Form):

    name = forms.CharField(label="name")
    #url = forms.URLField(label="url", initial="https://")
    description = forms.CharField()
    price = forms.FloatField()

    CATEGORIES = (
        ('Sports', 'SPO'),
        ('Racing', 'RAC'),
        ('RPG', 'RPG'),
        ( 'Action', 'ACT'),
        ( 'Adventure', 'ADV'),
        ( 'Casual', 'CAS'),
        ( 'Strategy', 'STR'),
        ('Other', 'OTH')
    )

    category = forms.ChoiceField(choices=CATEGORIES)

    class Meta:
        url = URLFieldForHTTPS

#Form for checking that the data is valid
#when the confirmation from the payment service
#is requested
class SuccessfulPaymentForm(forms.Form):
    pid = forms.CharField
    id = forms.IntegerField()
    ref = forms.CharField()
    result = forms.CharField()
    checksum = forms.CharField()


#Form for checking that the posted
#data is valid, used when modifing a game
class ModifyGameForm(forms.Form):
    gameid = forms.IntegerField()
    name = forms.CharField(label="name")
    url = forms.URLField(label="url")
    description = forms.CharField()
    price = forms.FloatField()

    CATEGORIES = (
        ('Sports', 'SPO'),
        ('Racing', 'RAC'),
        ('RPG', 'RPG'),
        ( 'Action', 'ACT'),
        ( 'Adventure', 'ADV'),
        ( 'Casual', 'CAS'),
        ( 'Strategy', 'STR'),
        ('Other', 'OTH')
    )

    category = forms.ChoiceField(choices=CATEGORIES)
