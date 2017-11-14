# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_author_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author_details',
            name='e_mail',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
