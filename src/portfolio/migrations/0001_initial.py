# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Symbol'
        db.create_table(u'portfolio_symbol', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('quote_symbol', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_quote_symbol', to=orm['portfolio.Symbol'])),
            ('longname', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'portfolio', ['Symbol'])

        # Adding model 'Holding'
        db.create_table(u'portfolio_holding', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('symbol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portfolio.Symbol'])),
            ('balance', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('iscash', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'portfolio', ['Holding'])

        # Adding model 'Return'
        db.create_table(u'portfolio_return', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('holding', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portfolio.Holding'])),
            ('period', self.gf('django.db.models.fields.IntegerField')()),
            ('irr', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal(u'portfolio', ['Return'])

        # Adding model 'Transaction'
        db.create_table(u'portfolio_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('to_holding', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transaction_set_to', null=True, to=orm['portfolio.Holding'])),
            ('from_holding', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transaction_set_from', null=True, to=orm['portfolio.Holding'])),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('shares', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=3, blank=True)),
            ('exchange_rate', self.gf('django.db.models.fields.DecimalField')(default=1.0, max_digits=12, decimal_places=4)),
            ('commission', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2, blank=True)),
            ('convAmount', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=12, decimal_places=2)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=12, decimal_places=2)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'portfolio', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Symbol'
        db.delete_table(u'portfolio_symbol')

        # Deleting model 'Holding'
        db.delete_table(u'portfolio_holding')

        # Deleting model 'Return'
        db.delete_table(u'portfolio_return')

        # Deleting model 'Transaction'
        db.delete_table(u'portfolio_transaction')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'portfolio.holding': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Holding'},
            'balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iscash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'symbol': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portfolio.Symbol']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'portfolio.return': {
            'Meta': {'ordering': "('holding',)", 'object_name': 'Return'},
            'holding': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portfolio.Holding']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'irr': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'period': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'portfolio.symbol': {
            'Meta': {'object_name': 'Symbol'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'longname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'quote_symbol': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_quote_symbol'", 'to': u"orm['portfolio.Symbol']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'portfolio.transaction': {
            'Meta': {'ordering': "('-date', 'notes')", 'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '12', 'decimal_places': '2'}),
            'commission': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'convAmount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '12', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'exchange_rate': ('django.db.models.fields.DecimalField', [], {'default': '1.0', 'max_digits': '12', 'decimal_places': '4'}),
            'from_holding': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transaction_set_from'", 'null': 'True', 'to': u"orm['portfolio.Holding']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '3', 'blank': 'True'}),
            'shares': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'to_holding': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transaction_set_to'", 'null': 'True', 'to': u"orm['portfolio.Holding']"}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['portfolio']
