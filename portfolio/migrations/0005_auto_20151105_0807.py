# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_remove_commodity_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='from_holding',
            field=models.ForeignKey(related_name='transaction_set_from', blank=True, to='portfolio.Holding', null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.IntegerField(choices=[(0, b'Buy'), (1, b'Sell'), (2, b'Dividend'), (3, b'Stock Split'), (4, b'Deposit')]),
        ),
    ]
