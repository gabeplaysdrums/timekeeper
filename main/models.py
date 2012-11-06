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

FEEL_NONE = '-'
FEEL_STRAIGHT = 'S'
FEEL_TRIPLET = 'T'
FEEL_SWING = 'W'

FEEL_CHOICES = (
  (FEEL_NONE, 'none'),
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

    # measures before changing the pattern
    MEASURES_PER_SECTION = 8

    # parts per down-beat
    ppd = int(PPQ * 4.0 / self.timesig_denom)

    class __Helper:
      def __init__(self, feel, ppd):
        self.feel = feel
        self.ppd = ppd
        self.default_dur = self.ppd
        if self.feel == FEEL_STRAIGHT:
          self.default_dur = self.ppd / 2
        elif self.feel == FEEL_TRIPLET:
          self.default_dur = self.ppd / 3
        elif self.feel == FEEL_SWING:
          self.default_dur = self.ppd / 3
        self.last_note = 0
        self.dur_remaining = 0
      def write_note(self, note, dur=None, rest=False):
        if rest:
          self.write_rest(dur)
          return
        if dur == None:
          dur = self.default_dur
        dur = max(0, dur)
        midi.note_on(channel=1, note=note)
        midi.update_time(dur)
        self.last_note = note
        self.dur_remaining -= dur
      def write_rest(self, dur=None):
        if dur == None:
          dur = self.default_dur
        dur = max(0, dur)
        midi.note_off(channel=1, note=self.last_note)
        midi.update_time(dur)
        self.dur_remaining -= dur
      def reset_downbeat(self):
        self.write_rest(self.dur_remaining)
        self.dur_remaining = self.ppd
      def write_accent(self, dur=None, rest=False):
        self.reset_downbeat()
        self.write_note(0x48, dur, rest)
      def write_downbeat(self, dur=None, rest=False):
        self.reset_downbeat()
        self.write_note(0x44, dur, rest)
      def write_upbeat(self, dur=None, rest=False):
        self.write_note(0x40, dur, rest)
      def write_feelbeats(self):
        if self.feel == FEEL_STRAIGHT:
          self.write_upbeat(self.dur_remaining)
        elif self.feel == FEEL_TRIPLET:
          self.write_upbeat()
          self.write_upbeat(self.dur_remaining)
        elif self.feel == FEEL_SWING:
          helper.write_rest()
          self.write_upbeat(self.dur_remaining)

    helper = __Helper(self.feel, ppd)
    del __Helper

    # Create sections
    #
    section_list = []

    class Section:
      def __init__(self):
        self.measures = 0
      def write(self):
        pass

    class FullSection(Section):
      def __init__(self, timesig_numer):
        self.measures = 1
        self.timesig_numer = timesig_numer
      def write(self):
        for i in range(self.timesig_numer):
          if i == 0:
            helper.write_accent()
          else:
            helper.write_downbeat()
          helper.write_feelbeats()

    section_list.append(FullSection(self.timesig_numer))

    class DownbeatSection(Section):
      def __init__(self, timesig_numer, downbeat_count):
        self.measures = 1
        self.timesig_numer = timesig_numer
        self.downbeat_count = downbeat_count
      def write(self):
        for i in range(self.timesig_numer):
          if i == 0:
            helper.write_accent()
          else:
            helper.write_downbeat()
          if i < self.downbeat_count:
            helper.write_feelbeats()

    for i in reversed(range(self.timesig_numer)):
      section_list.append(DownbeatSection(self.timesig_numer, i))

    class AccentSection(Section):
      def __init__(self, timesig_numer, downbeat_count):
        self.measures = 1
        self.timesig_numer = timesig_numer
        self.downbeat_count = downbeat_count
      def write(self):
        for i in range(self.timesig_numer):
          if i == 0:
            helper.write_accent()
          else:
            helper.write_downbeat(rest=(i >= self.downbeat_count))

    for i in reversed(range(1, self.timesig_numer)):
      section_list.append(AccentSection(self.timesig_numer, i))

    # non optional midi framework
    midi.header(format=0, nTracks=1, division=PPQ)
    midi.start_of_track() 
    midi.update_time(0)

    # non-musical events
    #

    timesig_denom_exp = int(math.log(self.timesig_denom, 2))
    midi.time_signature(self.timesig_numer, timesig_denom_exp, 24, 8)
    midi.tempo(int(60000000.00 / float(self.tempo)))
    
    # musical events
    #

    minutes_per_measure = self.timesig_numer / self.tempo
    total_minutes = 0
    section_count = 0

    while total_minutes < self.duration:
      section = section_list[section_count % len(section_list)]
      for i in range(0, MEASURES_PER_SECTION, section.measures):
        section.write()
        total_minutes += minutes_per_measure
      section_count += 1

    # non optional midi framework
    midi.update_time(0)
    midi.end_of_track() # not optional!
    midi.eof()

    file = open(path)
    self.midi_file.save(None, File(file))
    file.close()
    os.remove(path)
