# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_auto_20151103_0624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodity',
            name='quote_symbol',
            field=models.ForeignKey(related_name='related_quote_symbol', blank=True, to='portfolio.Commodity', null=True),
        ),
    ]
