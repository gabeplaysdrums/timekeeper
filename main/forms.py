from django import forms

class TimekeeperForm(forms.Form):
  tempo = forms.DecimalField(min_value=40, initial=120.0, decimal_places=1, widget=forms.TextInput(attrs={ 'size': '4' }))
  timesig_numer = forms.IntegerField(min_value=1, initial=4, widget=forms.TextInput(attrs={ 'size': '2' }))
  timesig_denom = forms.IntegerField(min_value=1, initial=4, widget=forms.TextInput(attrs={ 'size': '2' }))
  duration = forms.IntegerField(min_value=1, initial=2, widget=forms.TextInput(attrs={ 'size': '2' }))
