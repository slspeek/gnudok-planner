# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interval',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('begin', models.CharField(max_length=8, verbose_name='begin')),
                ('end', models.CharField(max_length=8, verbose_name='end')),
                ('region', models.ForeignKey(verbose_name='region', to='main.Region')),
            ],
        ),
    ]
