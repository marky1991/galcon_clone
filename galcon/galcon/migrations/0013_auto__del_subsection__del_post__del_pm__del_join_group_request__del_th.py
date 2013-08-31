# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Subsection'
        db.delete_table('galcon_subsection')

        # Deleting model 'Post'
        db.delete_table('galcon_post')

        # Deleting model 'Pm'
        db.delete_table('galcon_pm')

        # Deleting model 'Join_Group_Request'
        db.delete_table('galcon_join_group_request')

        # Deleting model 'Thread'
        db.delete_table('galcon_thread')

        # Deleting model 'Note'
        db.delete_table('galcon_note')

        # Deleting model 'Friend_Request'
        db.delete_table('galcon_friend_request')

        # Deleting model 'Section'
        db.delete_table('galcon_section')


    def backwards(self, orm):
        # Adding model 'Subsection'
        db.create_table('galcon_subsection', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', to=orm['galcon.Section'])),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100)),
        ))
        db.send_create_signal('galcon', ['Subsection'])

        # Adding model 'Post'
        db.create_table('galcon_post', (
            ('flag_note', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['galcon.Note'], null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', to=orm['galcon.Thread'])),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=65000)),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('last_modification_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['galcon.Player'])),
            ('title', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('galcon', ['Post'])

        # Adding model 'Pm'
        db.create_table('galcon_pm', (
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=65000)),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recieved_messages', to=orm['galcon.Player'])),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='written_messages', to=orm['galcon.Player'])),
            ('title', self.gf('django.db.models.fields.CharField')(default='(Blank)', max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('starred', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('galcon', ['Pm'])

        # Adding model 'Join_Group_Request'
        db.create_table('galcon_join_group_request', (
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_join_group_requests', to=orm['galcon.Player'])),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accepted', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='join_group_requests', to=orm['galcon.Player'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('galcon', ['Join_Group_Request'])

        # Adding model 'Thread'
        db.create_table('galcon_thread', (
            ('post_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', to=orm['galcon.Subsection'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='threads', to=orm['galcon.Player'])),
            ('close_note', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['galcon.Note'], null=True, blank=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sticky', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('page_views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100)),
        ))
        db.send_create_signal('galcon', ['Thread'])

        # Adding model 'Note'
        db.create_table('galcon_note', (
            ('text', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('galcon', ['Note'])

        # Adding model 'Friend_Request'
        db.create_table('galcon_friend_request', (
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_friend_requests', to=orm['galcon.Player'])),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accepted', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='friend_requests', to=orm['galcon.Player'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('galcon', ['Friend_Request'])

        # Adding model 'Section'
        db.create_table('galcon_section', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100)),
        ))
        db.send_create_signal('galcon', ['Section'])


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

    complete_apps = ['galcon']