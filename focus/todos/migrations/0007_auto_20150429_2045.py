# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0006_auto_20150429_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='text',
            field=models.CharField(default='TEST', max_length=200),
            preserve_default=False,
        ),
    ]
