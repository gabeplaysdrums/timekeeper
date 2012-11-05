from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from main.forms import *
from main.models import *

def index(request):
  form = None
  if request.method == 'POST':
    form = TimekeeperForm(request.POST)
    if form.is_valid():
      t = None
      try:
        t = Timekeeper.objects.get(
          timesig_numer=form.cleaned_data['timesig_numer'],
          timesig_denom=form.cleaned_data['timesig_denom'],
          tempo=form.cleaned_data['tempo'],
          duration=form.cleaned_data['duration'],
        )
      except Timekeeper.DoesNotExist:
        t = Timekeeper.objects.create(
          timesig_numer=form.cleaned_data['timesig_numer'],
          timesig_denom=form.cleaned_data['timesig_denom'],
          tempo=form.cleaned_data['tempo'],
          duration=form.cleaned_data['duration'],
        )
        t.generate_midi_file()
        t.save()
      return HttpResponseRedirect(t.midi_file.url)
  else:
    form = TimekeeperForm()
  return render_to_response(
    'index.html', 
    locals(),
    context_instance=RequestContext(request)
  )
