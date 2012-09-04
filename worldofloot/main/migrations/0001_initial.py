# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table('main_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('item_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('ilvl', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('quality', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('slot', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('wants', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('haves', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main', ['Item'])

        # Adding model 'Pin'
        db.create_table('main_pin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Item'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('session', self.gf('django.db.models.fields.CharField')(max_length=60, null=True)),
            ('verb', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('main', ['Pin'])

        # Adding model 'Image'
        db.create_table('main_image', (
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Item'])),
            ('image_id', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('thumb_path', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('attribution', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('priority', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('main', ['Image'])


    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table('main_item')

        # Deleting model 'Pin'
        db.delete_table('main_pin')

        # Deleting model 'Image'
        db.delete_table('main_image')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.image': {
            'Meta': {'object_name': 'Image'},
            'attribution': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'image_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Item']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'priority': ('django.db.models.fields.IntegerField', [], {}),
            'thumb_path': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'main.item': {
            'Meta': {'object_name': 'Item'},
            'haves': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ilvl': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'item_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'item_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'quality': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'wants': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.pin': {
            'Meta': {'object_name': 'Pin'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Item']"}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['main']