# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Add_Guest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=30)),
                ('e_mail', models.CharField(max_length=50, null=True)),
                ('event', models.ForeignKey(to='api.Add_Event')),
            ],
        ),
    ]
