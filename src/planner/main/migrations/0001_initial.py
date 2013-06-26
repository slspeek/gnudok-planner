# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Customer'
        db.create_table('main_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('additions', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('town', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('phone', self.gf('planner.main.models.PhoneNumberField')(max_length=20)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=120, blank=True)),
        ))
        db.send_create_signal('main', ['Customer'])

        # Adding unique constraint on 'Customer', fields ['postcode', 'number', 'additions']
        db.create_unique('main_customer', ['postcode', 'number', 'additions'])

        # Adding model 'TimeSlot'
        db.create_table('main_timeslot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day_of_week', self.gf('django.db.models.fields.IntegerField')()),
            ('begin', self.gf('django.db.models.fields.FloatField')()),
            ('end', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('main', ['TimeSlot'])

        # Adding model 'Region'
        db.create_table('main_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('main', ['Region'])

        # Adding model 'Car'
        db.create_table('main_car', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('main', ['Car'])

        # Adding model 'Rule'
        db.create_table('main_rule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('car', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Car'])),
            ('timeslot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.TimeSlot'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Region'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('main', ['Rule'])

        # Adding model 'Calendar'
        db.create_table('main_calendar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('car', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Car'])),
            ('timeslot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.TimeSlot'])),
        ))
        db.send_create_signal('main', ['Calendar'])

        # Adding unique constraint on 'Calendar', fields ['date', 'car', 'timeslot']
        db.create_unique('main_calendar', ['date', 'car_id', 'timeslot_id'])

        # Adding model 'Appointment'
        db.create_table('main_appointment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('calendar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Calendar'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Customer'])),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('kind', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('weight', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('stuff', self.gf('django.db.models.fields.TextField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 11, 0, 0))),
        ))
        db.send_create_signal('main', ['Appointment'])


    def backwards(self, orm):
        # Removing unique constraint on 'Calendar', fields ['date', 'car', 'timeslot']
        db.delete_unique('main_calendar', ['date', 'car_id', 'timeslot_id'])

        # Removing unique constraint on 'Customer', fields ['postcode', 'number', 'additions']
        db.delete_unique('main_customer', ['postcode', 'number', 'additions'])

        # Deleting model 'Customer'
        db.delete_table('main_customer')

        # Deleting model 'TimeSlot'
        db.delete_table('main_timeslot')

        # Deleting model 'Region'
        db.delete_table('main_region')

        # Deleting model 'Car'
        db.delete_table('main_car')

        # Deleting model 'Rule'
        db.delete_table('main_rule')

        # Deleting model 'Calendar'
        db.delete_table('main_calendar')

        # Deleting model 'Appointment'
        db.delete_table('main_appointment')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.appointment': {
            'Meta': {'ordering': "['customer__postcode']", 'object_name': 'Appointment'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Calendar']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 11, 0, 0)'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Customer']"}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'stuff': ('django.db.models.fields.TextField', [], {}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'main.calendar': {
            'Meta': {'ordering': "['date', 'timeslot__begin']", 'unique_together': "(('date', 'car', 'timeslot'),)", 'object_name': 'Calendar'},
            'car': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Car']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timeslot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.TimeSlot']"})
        },
        'main.car': {
            'Meta': {'object_name': 'Car'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'main.customer': {
            'Meta': {'unique_together': "(('postcode', 'number', 'additions'),)", 'object_name': 'Customer'},
            'additions': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '120', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'phone': ('planner.main.models.PhoneNumberField', [], {'max_length': '20'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'main.region': {
            'Meta': {'object_name': 'Region'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'})
        },
        'main.rule': {
            'Meta': {'object_name': 'Rule'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'car': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Car']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Region']"}),
            'timeslot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.TimeSlot']"})
        },
        'main.timeslot': {
            'Meta': {'object_name': 'TimeSlot'},
            'begin': ('django.db.models.fields.FloatField', [], {}),
            'day_of_week': ('django.db.models.fields.IntegerField', [], {}),
            'end': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['main']