# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('longname', models.CharField(max_length=100)),
                ('quote_symbol', models.ForeignKey(related_name='related_quote_symbol', to='portfolio.Commodity')),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'commodity/currency',
                'verbose_name_plural': 'commodities/currencies',
            },
        ),
        migrations.RemoveField(
            model_name='symbol',
            name='quote_symbol',
        ),
        migrations.RemoveField(
            model_name='symbol',
            name='user',
        ),
        migrations.AlterField(
            model_name='holding',
            name='symbol',
            field=models.ForeignKey(to='portfolio.Commodity'),
        ),
        migrations.DeleteModel(
            name='Symbol',
        ),
    ]
