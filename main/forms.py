from django import forms
from main.models import *

class TimekeeperForm(forms.Form):
  tempo = forms.DecimalField(min_value=40, initial=120.0, decimal_places=1, widget=forms.TextInput(attrs={ 'size': '4' }))
  timesig_numer = forms.IntegerField(min_value=1, initial=4, widget=forms.TextInput(attrs={ 'size': '2' }))
  timesig_denom = forms.TypedChoiceField(choices=(('4', '4'), ('8', '8')), coerce=int)
  duration = forms.IntegerField(min_value=1, initial=2, widget=forms.TextInput(attrs={ 'size': '2' }))
  feel = forms.ChoiceField(choices=FEEL_CHOICES, initial=FEEL_STRAIGHT)
  measures_per_phrase = forms.IntegerField(min_value=1, initial=4, widget=forms.TextInput(attrs={ 'size': '2' }))
