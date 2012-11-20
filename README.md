timekeeper
==========

scripts for creating practice tracks to work on musical timekeeping

Python Midi Library:
http://www.mxm.dk/products/public/pythonmidi/

Django 1.4.2:
https://www.djangoproject.com/

South 0.7.6:
http://south.aeracode.org/

Initial setup:
$ python manage.py syncdb
$ python manage.py collectstatic
$ python manage.py migrate main

Using local webserver on Windows:
> start cmd
> python manage.py runserver
