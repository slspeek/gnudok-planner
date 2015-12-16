# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Interval'
        db.create_table('area_interval', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('begin', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('end', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Region'])),
        ))
        db.send_create_signal('area', ['Interval'])


    def backwards(self, orm):
        # Deleting model 'Interval'
        db.delete_table('area_interval')


    models = {
        'area.interval': {
            'Meta': {'object_name': 'Interval'},
            'begin': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'end': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Region']"})
        },
        'main.region': {
            'Meta': {'object_name': 'Region'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'})
        }
    }

    complete_apps = ['area']