from django.core.files import File
from django.db import models
from midi.MidiOutFile import MidiOutFile
import os
import tempfile
import math

class ModelBase(models.Model):
  created = models.DateField(auto_now_add=True)
  modified = models.DateField(auto_now=True)
  class Meta:
    abstract = True

FEEL_STRAIGHT = 'S'
FEEL_TRIPLET = 'T'
FEEL_SWING = 'W'

FEEL_CHOICES = (
  (FEEL_STRAIGHT, 'straight'),
  (FEEL_TRIPLET, 'triplet'),
  (FEEL_SWING, 'swing'),
)

class Timekeeper(ModelBase):
  tempo = models.DecimalField(decimal_places=1, max_digits=4)
  timesig_numer = models.IntegerField()
  timesig_denom = models.IntegerField()
  duration = models.IntegerField()
  feel = models.CharField(max_length=1, default=FEEL_STRAIGHT, choices=FEEL_CHOICES)
  request_count = models.PositiveIntegerField(default=0)

  def compute_file_path(instance, filename):
    return 'timekeeper_%d-%d_%s_%.1f_bpm_%d_minutes.mid' % (
      instance.timesig_numer,
      instance.timesig_denom,
      instance.get_feel_display(),
      instance.tempo,
      instance.duration,
    )

  midi_file = models.FileField(upload_to=compute_file_path)

  def generate_midi_file(self):
    (f, path) = tempfile.mkstemp()
    os.close(f)
    midi = MidiOutFile(path)

    # parts per quarter-note
    PPQ = 96

    # parts per down-beat
    ppd = int(PPQ * 4.0 / self.timesig_denom)
    
    # non optional midi framework
    midi.header(format=0, nTracks=1, division=PPQ)
    midi.start_of_track() 
    midi.update_time(0)

    NOTE_ACCENT = 'a'
    NOTE_DOWNBEAT = 'd'
    NOTE_UPBEAT = 'u'
    NOTE_REST = '-'

    note_list = []

    for i in range(self.timesig_numer):
      downbeat = NOTE_DOWNBEAT
      if i == 0:
        downbeat = NOTE_ACCENT
      if self.feel == FEEL_STRAIGHT:
        note_list.append(downbeat)
        note_list.append(NOTE_UPBEAT)
      elif self.feel == FEEL_TRIPLET:
        note_list.append(downbeat)
        note_list.append(NOTE_UPBEAT)
        note_list.append(NOTE_UPBEAT)
      elif self.feel == FEEL_SWING:
        note_list.append(downbeat)
        note_list.append(NOTE_REST)
        note_list.append(NOTE_UPBEAT)

    note_step = None
    if self.feel == FEEL_STRAIGHT:
      note_step = ppd / 2
    elif self.feel == FEEL_TRIPLET:
      note_step = ppd / 3
    elif self.feel == FEEL_SWING:
      note_step = ppd / 3

    # non-musical events
    #

    timesig_denom_exp = int(math.log(self.timesig_denom, 2))
    midi.time_signature(self.timesig_numer, timesig_denom_exp, 24, 8)
    midi.tempo(int(60000000.00 / float(self.tempo)))
    
    # musical events
    #

    minutes_per_measure = self.timesig_numer / self.tempo
    total_minutes = 0
    last_note = None

    while total_minutes < self.duration:
      for n in note_list:
        if n == NOTE_REST:
          midi.note_off(channel=1, note=last_note)
        elif n == NOTE_ACCENT:
          midi.note_on(channel=1, note=0x48)
          last_note = 0x48
        elif n == NOTE_DOWNBEAT:
          midi.note_on(channel=1, note=0x44)
          last_note = 0x44
        else:
          midi.note_on(channel=1, note=0x40)
          last_note = 0x40
        midi.update_time(note_step)
      total_minutes += minutes_per_measure

    # non optional midi framework
    midi.update_time(0)
    midi.end_of_track() # not optional!
    midi.eof()

    file = open(path)
    self.midi_file.save(None, File(file))
    file.close()
    os.remove(path)
