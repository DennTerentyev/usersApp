# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_auto_20170811_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='by_invite_code',
        ),
    ]
