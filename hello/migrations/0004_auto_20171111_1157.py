# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_auto_20171111_1146'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('publication', models.DateField()),
                ('author', models.ManyToManyField(to='hello.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=10)),
                ('website', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='author_details',
            name='e_mail',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='author_details',
            name='sex',
            field=models.SmallIntegerField(choices=[(0, b'\xe7\x94\xb7'), (1, b'\xe5\xa5\xb3')]),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(to='hello.Publisher'),
        ),
    ]
