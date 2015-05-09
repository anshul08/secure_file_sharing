# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filelink',
            options={'verbose_name': 'file_link'},
        ),
    ]
