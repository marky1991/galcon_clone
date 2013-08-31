# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Line'
        db.create_table('chat_line', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author_name', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=100)),
        ))
        db.send_create_signal('chat', ['Line'])


    def backwards(self, orm):
        # Deleting model 'Line'
        db.delete_table('chat_line')


    models = {
        'chat.line': {
            'Meta': {'ordering': "['post_date']", 'object_name': 'Line'},
            'author_name': ('django.db.models.fields.TextField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['chat']