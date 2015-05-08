# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('externalName', models.CharField(max_length=200)),
                ('linkSuffix', models.CharField(max_length=200)),
                ('created_on', models.DateTimeField(verbose_name=b'date published')),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
