from django import forms

#Form for adding new game
class NewGameForm(forms.Form):
    name = forms.CharField(label="name")
    url = forms.URLField(label="url")
    description = forms.CharField()
    price = forms.FloatField()
