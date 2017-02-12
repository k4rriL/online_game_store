from django import forms

#Form for checking that the posted
#data is valid, used when adding a new game
class AddGameForm(forms.Form):
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
