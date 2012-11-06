from django.core.management.base import BaseCommand, CommandError
from main.models import *

class Command(BaseCommand):
  args = ''
  help = 'deletes cached midi files'

  def handle(self, *args, **options):
    for t in Timekeeper.objects.all():
      if t.midi_file:
        t.midi_file.delete()
