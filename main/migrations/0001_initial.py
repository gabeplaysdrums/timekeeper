# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Timekeeper'
        db.create_table('main_timekeeper', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('tempo', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=1)),
            ('timesig_numer', self.gf('django.db.models.fields.IntegerField')()),
            ('timesig_denom', self.gf('django.db.models.fields.IntegerField')()),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('feel', self.gf('django.db.models.fields.CharField')(default='S', max_length=1)),
            ('measures_per_phrase', self.gf('django.db.models.fields.IntegerField')()),
            ('request_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('midi_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('main', ['Timekeeper'])


    def backwards(self, orm):
        # Deleting model 'Timekeeper'
        db.delete_table('main_timekeeper')


    models = {
        'main.timekeeper': {
            'Meta': {'object_name': 'Timekeeper'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'feel': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measures_per_phrase': ('django.db.models.fields.IntegerField', [], {}),
            'midi_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'request_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'tempo': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '1'}),
            'timesig_denom': ('django.db.models.fields.IntegerField', [], {}),
            'timesig_numer': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['main']