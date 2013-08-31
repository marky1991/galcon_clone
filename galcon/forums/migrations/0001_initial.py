# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Note'
        db.create_table('forums_note', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=100)),
        ))
        db.send_create_signal('forums', ['Note'])

        # Adding model 'Section'
        db.create_table('forums_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('forums', ['Section'])

        # Adding model 'Subsection'
        db.create_table('forums_subsection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', to=orm['forums.Section'])),
        ))
        db.send_create_signal('forums', ['Subsection'])

        # Adding model 'Thread'
        db.create_table('forums_thread', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='threads', to=orm['galcon.Player'])),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', to=orm['forums.Subsection'])),
            ('close_note', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forums.Note'], null=True, blank=True)),
            ('sticky', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('page_views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('forums', ['Thread'])

        # Adding model 'Post'
        db.create_table('forums_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100)),
            ('title', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['galcon.Player'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', to=orm['forums.Thread'])),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('last_modification_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=65000)),
            ('flag_note', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forums.Note'], null=True, blank=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('forums', ['Post'])


    def backwards(self, orm):
        # Deleting model 'Note'
        db.delete_table('forums_note')

        # Deleting model 'Section'
        db.delete_table('forums_section')

        # Deleting model 'Subsection'
        db.delete_table('forums_subsection')

        # Deleting model 'Thread'
        db.delete_table('forums_thread')

        # Deleting model 'Post'
        db.delete_table('forums_post')


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
        'forums.note': {
            'Meta': {'object_name': 'Note'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        },
        'forums.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['galcon.Player']"}),
            'flag_note': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forums.Note']", 'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modification_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'to': "orm['forums.Thread']"}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '65000'}),
            'title': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        },
        'forums.section': {
            'Meta': {'object_name': 'Section'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        },
        'forums.subsection': {
            'Meta': {'object_name': 'Subsection'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'to': "orm['forums.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        },
        'forums.thread': {
            'Meta': {'object_name': 'Thread'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'threads'", 'to': "orm['galcon.Player']"}),
            'close_note': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forums.Note']", 'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'to': "orm['forums.Subsection']"}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'galcon.player': {
            'Meta': {'object_name': 'Player'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'friends_rel_+'", 'blank': 'True', 'to': "orm['galcon.Player']"}),
            'get_newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'groups'", 'blank': 'True', 'to': "orm['groups.Group']"}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'post_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rank': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['galcon.Rank']", 'unique': 'True'}),
            'registration_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'registration_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'}),
            'trophies': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'players'", 'blank': 'True', 'to': "orm['galcon.Trophy']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'galcon.rank': {
            'Meta': {'object_name': 'Rank'},
            'classic_rank': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'flash_rank': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fusion_rank': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iphone_rank': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'galcon.trophy': {
            'Meta': {'object_name': 'Trophy'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        },
        'groups.group': {
            'Meta': {'object_name': 'Group'},
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'admined_groups'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['galcon.Player']"}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '65000'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_requires_approval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['forums']