# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
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
            options={
                'verbose_name_plural': 'currencies',
            },
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
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dividend',
            fields=[
                ('transaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='portfolio.Transaction')),
                ('exchange_rate', models.DecimalField(default=1.0, null=True, max_digits=12, decimal_places=4, blank=True)),
                ('original_amount', models.DecimalField(default=0.0, max_digits=12, decimal_places=2)),
                ('total_amount', models.DecimalField(default=0.0, max_digits=12, decimal_places=2)),
            ],
            options={
                'abstract': False,
            },
            bases=('portfolio.transaction',),
        ),
        migrations.CreateModel(
            name='StockSplit',
            fields=[
                ('transaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='portfolio.Transaction')),
                ('share_multiplier', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('portfolio.transaction',),
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('transaction_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='portfolio.Transaction')),
                ('exchange_rate', models.DecimalField(default=1.0, null=True, max_digits=12, decimal_places=4, blank=True)),
                ('original_amount', models.DecimalField(default=0.0, max_digits=12, decimal_places=2)),
                ('total_amount', models.DecimalField(default=0.0, max_digits=12, decimal_places=2)),
                ('type', models.IntegerField(choices=[(0, b'Buy'), (1, b'Sell')])),
                ('number_of_shares', models.DecimalField(max_digits=12, decimal_places=2)),
                ('price', models.DecimalField(max_digits=12, decimal_places=3)),
                ('commission', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('notes', models.CharField(max_length=100, blank=True)),
            ],
            options={
                'ordering': ('-date', 'notes'),
                'get_latest_by': 'date',
            },
            bases=('portfolio.transaction',),
        ),
        migrations.AddField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(to='portfolio.Account'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_portfolio.transaction_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='stock',
            field=models.ForeignKey(to='portfolio.Stock'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
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
        migrations.AddField(
            model_name='account',
            name='currency',
            field=models.ForeignKey(to='portfolio.Currency'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
