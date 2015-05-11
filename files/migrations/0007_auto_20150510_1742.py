# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0006_filelink_linksuffix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filelink',
            name='created_on',
            field=models.DateTimeField(verbose_name=b'date created'),
        ),
        migrations.AlterField(
            model_name='filelink',
            name='linkSuffix',
            field=models.CharField(default=b'', unique=True, max_length=200),
        ),
    ]
