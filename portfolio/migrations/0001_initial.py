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
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('currency', models.ForeignKey(to='portfolio.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance', models.DecimalField(max_digits=12, decimal_places=2)),
                ('account', models.ForeignKey(to='portfolio.Account')),
            ],
            options={
                'ordering': ('account', 'stock', 'balance'),
            },
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period', models.IntegerField(choices=[(0, b'all time')])),
                ('irr', models.DecimalField(max_digits=12, decimal_places=2)),
                ('position', models.ForeignKey(to='portfolio.Position')),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'Annualized Return',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('symbol', models.CharField(max_length=20)),
                ('quote_symbol', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('exchange', models.ForeignKey(to='portfolio.Exchange')),
            ],
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(choices=[(0, b'Buy'), (1, b'Sell')])),
                ('date', models.DateField()),
                ('numshares', models.DecimalField(max_digits=12, decimal_places=2)),
                ('price', models.DecimalField(max_digits=12, decimal_places=3)),
                ('exchange_rate', models.DecimalField(default=1.0, max_digits=12, decimal_places=4)),
                ('commission', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('convAmount', models.DecimalField(default=0.0, max_digits=12, decimal_places=2)),
                ('amount', models.DecimalField(default=0.0, max_digits=12, decimal_places=2)),
                ('notes', models.CharField(max_length=100, blank=True)),
                ('account', models.ForeignKey(to='portfolio.Account')),
                ('stock', models.ForeignKey(to='portfolio.Stock')),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date', 'notes'),
                'get_latest_by': 'date',
            },
        ),
        migrations.AddField(
            model_name='position',
            name='stock',
            field=models.ForeignKey(to='portfolio.Stock'),
        ),
        migrations.AddField(
            model_name='position',
            name='user',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
