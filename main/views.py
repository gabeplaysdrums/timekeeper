from django.shortcuts import render_to_response
from django.template import RequestContext
from main.forms import *

def index(request):
  form = TimekeeperForm()
  return render_to_response(
    'index.html', 
    locals(), 
    context_instance=RequestContext(request)
  )
