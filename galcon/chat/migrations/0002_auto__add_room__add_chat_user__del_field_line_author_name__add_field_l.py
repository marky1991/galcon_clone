# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Room'
        db.create_table('chat_room', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=50)),
        ))
        db.send_create_signal('chat', ['Room'])

        # Adding M2M table for field users on 'Room'
        m2m_table_name = db.shorten_name('chat_room_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('room', models.ForeignKey(orm['chat.room'], null=False)),
            ('chat_user', models.ForeignKey(orm['chat.chat_user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['room_id', 'chat_user_id'])

        # Adding M2M table for field admins on 'Room'
        m2m_table_name = db.shorten_name('chat_room_admins')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('room', models.ForeignKey(orm['chat.room'], null=False)),
            ('chat_user', models.ForeignKey(orm['chat.chat_user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['room_id', 'chat_user_id'])

        # Adding model 'Chat_User'
        db.create_table('chat_chat_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='chat_user', unique=True, to=orm['auth.User'])),
            ('last_seen_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('chat', ['Chat_User'])

        # Deleting field 'Line.author_name'
        db.delete_column('chat_line', 'author_name')

        # Adding field 'Line.author'
        db.add_column('chat_line', 'author',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['chat.Chat_User']),
                      keep_default=False)

        # Adding field 'Line.room'
        db.add_column('chat_line', 'room',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='lines', to=orm['chat.Room']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Room'
        db.delete_table('chat_room')

        # Removing M2M table for field users on 'Room'
        db.delete_table(db.shorten_name('chat_room_users'))

        # Removing M2M table for field admins on 'Room'
        db.delete_table(db.shorten_name('chat_room_admins'))

        # Deleting model 'Chat_User'
        db.delete_table('chat_chat_user')

        # Adding field 'Line.author_name'
        db.add_column('chat_line', 'author_name',
                      self.gf('django.db.models.fields.TextField')(default=1, max_length=100),
                      keep_default=False)

        # Deleting field 'Line.author'
        db.delete_column('chat_line', 'author_id')

        # Deleting field 'Line.room'
        db.delete_column('chat_line', 'room_id')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'chat.chat_user': {
            'Meta': {'object_name': 'Chat_User'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seen_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'chat_user'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'chat.line': {
            'Meta': {'ordering': "['post_date']", 'object_name': 'Line'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chat.Chat_User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lines'", 'to': "orm['chat.Room']"}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        },
        'chat.room': {
            'Meta': {'object_name': 'Room'},
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'admined_chat_rooms'", 'symmetrical': 'False', 'to': "orm['chat.Chat_User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '50'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'chat_rooms'", 'symmetrical': 'False', 'to': "orm['chat.Chat_User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['chat']