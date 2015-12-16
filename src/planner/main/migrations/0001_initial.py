# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import planner.main.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.IntegerField(default=2, verbose_name='kind', choices=[(1, 'Delivery'), (2, 'Pick up')])),
                ('status', models.IntegerField(default=1, verbose_name='status', choices=[(1, 'Normal'), (2, 'Cancelled')])),
                ('weight', models.IntegerField(default=1, verbose_name='weight', choices=[(1, 'Normal'), (2, 'Double'), (3, 'Tripel'), (4, 'Entire half-day')])),
                ('stuff', models.TextField(verbose_name='stuff')),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created')),
            ],
            options={
                'ordering': ['kind', 'customer__postcode'],
            },
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='date')),
            ],
            options={
                'ordering': ['date', 'timeslot__begin'],
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postcode', models.CharField(max_length=14, verbose_name='postalcode')),
                ('number', models.CharField(max_length=10, verbose_name='number')),
                ('additions', models.CharField(max_length=10, verbose_name='additions', blank=True)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('address', models.CharField(max_length=120, verbose_name='address')),
                ('town', models.CharField(max_length=120, verbose_name='town')),
                ('phone', planner.main.models.PhoneNumberField(max_length=20)),
                ('email', models.EmailField(max_length=120, verbose_name='email', blank=True)),
            ],
            options={
                'permissions': (('viewers', 'Viewers'), ('callcenter', 'Callcenter')),
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=120, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.IntegerField(default=2, verbose_name='kind', choices=[(1, 'Delivery'), (2, 'Pick up')])),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('car', models.ForeignKey(verbose_name='car', to='main.Car')),
                ('region', models.ForeignKey(verbose_name='region', to='main.Region')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day_of_week', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday')])),
                ('begin', models.FloatField()),
                ('end', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='rule',
            name='timeslot',
            field=models.ForeignKey(verbose_name='timeslot', to='main.TimeSlot'),
        ),
        migrations.AlterUniqueTogether(
            name='customer',
            unique_together=set([('postcode', 'number', 'additions')]),
        ),
        migrations.AddField(
            model_name='calendar',
            name='car',
            field=models.ForeignKey(verbose_name='car', to='main.Car'),
        ),
        migrations.AddField(
            model_name='calendar',
            name='timeslot',
            field=models.ForeignKey(verbose_name='timeslot', to='main.TimeSlot'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='calendar',
            field=models.ForeignKey(verbose_name='calendar', to='main.Calendar'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='customer',
            field=models.ForeignKey(verbose_name='customer', to='main.Customer'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='employee',
            field=models.ForeignKey(verbose_name='employee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='calendar',
            unique_together=set([('date', 'car', 'timeslot')]),
        ),
    ]
