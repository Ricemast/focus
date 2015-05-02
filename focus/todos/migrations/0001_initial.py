# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(default=b'New Todo', max_length=200)),
                ('priority', models.IntegerField(null=True, blank=True)),
                ('complete', models.BooleanField(default=False)),
            ],
        ),
    ]
