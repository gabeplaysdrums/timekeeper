import os 
import sys 
 
production = os.path.dirname(globals()['__file__']) 
project = os.path.dirname(production) 
workspace = os.path.dirname(project) 

if project not in sys.path: 
  sys.path.append(project) 
if workspace not in sys.path: 
  sys.path.append(workspace) 
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'timekeeper.production.settings' 
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
from django.core.handlers.wsgi import WSGIHandler 
application = WSGIHandler() 
