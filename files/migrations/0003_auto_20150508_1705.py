# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_auto_20150508_1704'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filelink',
            options={},
        ),
        migrations.AlterModelTable(
            name='filelink',
            table='file_link',
        ),
    ]
