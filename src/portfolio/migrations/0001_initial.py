# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Symbol'
        db.create_table('portfolio_symbol', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('portfolio', ['Symbol'])

        # Adding model 'Holding'
        db.create_table('portfolio_holding', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('symbol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portfolio.Symbol'])),
            ('balance', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('tags', self.gf('tagging.fields.TagField')()),
        ))
        db.send_create_signal('portfolio', ['Holding'])

        # Adding model 'Return'
        db.create_table('portfolio_return', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('holding', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portfolio.Holding'])),
            ('period', self.gf('django.db.models.fields.IntegerField')()),
            ('irr', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal('portfolio', ['Return'])

        # Adding model 'Transaction'
        db.create_table('portfolio_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to_holding', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transaction_set_to', null=True, to=orm['portfolio.Holding'])),
            ('from_holding', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transaction_set_from', null=True, to=orm['portfolio.Holding'])),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('shares', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('exchange_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('commission', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=12, decimal_places=2)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('portfolio', ['Transaction'])


    def backwards(self, orm):
        
        # Deleting model 'Symbol'
        db.delete_table('portfolio_symbol')

        # Deleting model 'Holding'
        db.delete_table('portfolio_holding')

        # Deleting model 'Return'
        db.delete_table('portfolio_return')

        # Deleting model 'Transaction'
        db.delete_table('portfolio_transaction')


    models = {
        'portfolio.holding': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Holding'},
            'balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'symbol': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['portfolio.Symbol']"}),
            'tags': ('tagging.fields.TagField', [], {})
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
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'portfolio.transaction': {
            'Meta': {'ordering': "('-date', 'notes')", 'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '12', 'decimal_places': '2'}),
            'commission': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'exchange_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'from_holding': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transaction_set_from'", 'null': 'True', 'to': "orm['portfolio.Holding']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'shares': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'to_holding': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transaction_set_to'", 'null': 'True', 'to': "orm['portfolio.Holding']"}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['portfolio']
