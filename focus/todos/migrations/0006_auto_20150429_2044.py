# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0005_auto_20150429_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='text',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
