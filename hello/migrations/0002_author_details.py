# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author_Details',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sex', models.SmallIntegerField()),
                ('age', models.SmallIntegerField()),
                ('e_mail', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('author', models.OneToOneField(to='hello.Author')),
            ],
        ),
    ]
