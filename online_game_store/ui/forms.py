from django import forms

#Form for adding new game
class NewGameForm(forms.Form):
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
