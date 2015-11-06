# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('balance', models.DecimalField(max_digits=12, decimal_places=2)),
                ('iscash', models.BooleanField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period', models.IntegerField(choices=[(0, b'all time')])),
                ('irr', models.DecimalField(max_digits=12, decimal_places=2)),
                ('holding', models.ForeignKey(to='portfolio.Holding')),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('holding',),
                'verbose_name': 'Annualized Return',
            },
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('longname', models.CharField(max_length=100)),
                ('quote_symbol', models.ForeignKey(related_name='related_quote_symbol', to='portfolio.Symbol')),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'symbol/currency',
                'verbose_name_plural': 'symbols/currencies',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(choices=[(0, b'Buy'), (1, b'Sell'), (2, b'Dividend'), (3, b'Stock Split')])),
                ('date', models.DateField()),
                ('shares', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('price', models.DecimalField(null=True, max_digits=12, decimal_places=3, blank=True)),
                ('exchange_rate', models.DecimalField(default=1.0, max_digits=12, decimal_places=4)),
                ('commission', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('convAmount', models.DecimalField(default=0.0, max_digits=12, decimal_places=2)),
                ('amount', models.DecimalField(default=0.0, max_digits=12, decimal_places=2)),
                ('notes', models.CharField(max_length=100, blank=True)),
                ('from_holding', models.ForeignKey(related_name='transaction_set_from', to='portfolio.Holding', null=True)),
                ('to_holding', models.ForeignKey(related_name='transaction_set_to', to='portfolio.Holding', null=True)),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date', 'notes'),
                'get_latest_by': 'date',
            },
        ),
        migrations.AddField(
            model_name='holding',
            name='symbol',
            field=models.ForeignKey(to='portfolio.Symbol'),
        ),
        migrations.AddField(
            model_name='holding',
            name='user',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
