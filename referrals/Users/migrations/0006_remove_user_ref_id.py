# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_auto_20170815_0811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='ref_id',
        ),
    ]
