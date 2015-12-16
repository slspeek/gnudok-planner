# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Rule.kind'
        db.add_column(u'main_rule', 'kind',
                      self.gf('django.db.models.fields.IntegerField')(default=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Rule.kind'
        db.delete_column(u'main_rule', 'kind')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.appointment': {
            'Meta': {'ordering': "['kind', 'customer__postcode']", 'object_name': 'Appointment'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Calendar']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 21, 0, 0)'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Customer']"}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'stuff': ('django.db.models.fields.TextField', [], {}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'main.calendar': {
            'Meta': {'ordering': "['date', 'timeslot__begin']", 'unique_together': "(('date', 'car', 'timeslot'),)", 'object_name': 'Calendar'},
            'car': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Car']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timeslot': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.TimeSlot']"})
        },
        u'main.car': {
            'Meta': {'object_name': 'Car'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'main.customer': {
            'Meta': {'unique_together': "(('postcode', 'number', 'additions'),)", 'object_name': 'Customer'},
            'additions': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '120', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'phone': ('planner.main.models.PhoneNumberField', [], {'max_length': '20'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'main.region': {
            'Meta': {'object_name': 'Region'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'})
        },
        u'main.rule': {
            'Meta': {'object_name': 'Rule'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'car': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Car']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Region']"}),
            'timeslot': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.TimeSlot']"})
        },
        u'main.timeslot': {
            'Meta': {'object_name': 'TimeSlot'},
            'begin': ('django.db.models.fields.FloatField', [], {}),
            'day_of_week': ('django.db.models.fields.IntegerField', [], {}),
            'end': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['main']