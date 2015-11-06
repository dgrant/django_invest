# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_auto_20151103_0630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commodity',
            name='user',
        ),
    ]
