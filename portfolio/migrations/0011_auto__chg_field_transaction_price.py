# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Transaction.price'
        db.alter_column('portfolio_transaction', 'price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=3))

    def backwards(self, orm):

        # Changing field 'Transaction.price'
        db.alter_column('portfolio_transaction', 'price', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=12, decimal_places=3))

    models = {
        'portfolio.holding': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Holding'},
            'balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'symbol': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['portfolio.Symbol']"})
        },
        'portfolio.return': {
            'Meta': {'ordering': "('holding',)", 'object_name': 'Return'},
            'holding': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['portfolio.Holding']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irr': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'period': ('django.db.models.fields.IntegerField', [], {})
        },
        'portfolio.symbol': {
            'Meta': {'object_name': 'Symbol'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'longname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'quote_symbol': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_quote_symbol'", 'to': "orm['portfolio.Symbol']"})
        },
        'portfolio.transaction': {
            'Meta': {'ordering': "('-date', 'notes')", 'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '12', 'decimal_places': '2'}),
            'commission': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'convAmount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '12', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'exchange_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'from_holding': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transaction_set_from'", 'null': 'True', 'to': "orm['portfolio.Holding']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '3'}),
            'shares': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'to_holding': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transaction_set_to'", 'null': 'True', 'to': "orm['portfolio.Holding']"}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['portfolio']