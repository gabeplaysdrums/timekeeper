from timekeeper.settings import *

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'timekeeper',
        'USER': 'timekeeper',
        'PASSWORD': 'groovin',
        'HOST': '',
        'PORT': '',
    }
}
