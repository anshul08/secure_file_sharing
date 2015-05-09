# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_auto_20150508_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='filelink',
            name='password_protected',
            field=models.BooleanField(default=False),
        ),
    ]
