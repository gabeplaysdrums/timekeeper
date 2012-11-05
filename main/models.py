from django.core.files import File
from django.db import models
from midi.MidiOutFile import MidiOutFile
import os
import tempfile

class ModelBase(models.Model):
  created = models.DateField(auto_now_add=True)
  modified = models.DateField(auto_now=True)
  class Meta:
    abstract = True

class Timekeeper(ModelBase):
  tempo = models.DecimalField(decimal_places=1, max_digits=4)
  timesig_numer = models.IntegerField()
  timesig_denom = models.IntegerField()
  duration = models.IntegerField()

  def compute_file_path(instance, filename):
    return 'timekeeper_%d-%d_%.1f_bpm_%d_minutes.mid' % (
      instance.timesig_numer,
      instance.timesig_denom,
      instance.tempo,
      instance.duration,
    )

  midi_file = models.FileField(upload_to=compute_file_path)

  def generate_midi_file(self):
    (f, path) = tempfile.mkstemp()
    os.close(f)
    midi = MidiOutFile(path)
    
    # non optional midi framework
    midi.header()
    midi.start_of_track() 
    
    # musical events
    midi.update_time(0)
    midi.note_on(channel=0, note=0x40)
    
    midi.update_time(192)
    midi.note_off(channel=0, note=0x40)
    
    # non optional midi framework
    midi.update_time(0)
    midi.end_of_track() # not optional!
    
    midi.eof()

    file = open(path)
    self.midi_file.save(None, File(file))
    file.close()
    os.remove(path)
