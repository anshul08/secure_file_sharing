# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0005_remove_filelink_linksuffix'),
    ]

    operations = [
        migrations.AddField(
            model_name='filelink',
            name='linkSuffix',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
