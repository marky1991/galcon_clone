# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rank'
        db.create_table('galcon_rank', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iphone_rank', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('classic_rank', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('flash_rank', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fusion_rank', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('galcon', ['Rank'])

        # Adding model 'Player'
        db.create_table('galcon_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100)),
            ('post_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('rank', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['galcon.Rank'], unique=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('registration_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('registration_code', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
        ))
        db.send_create_signal('galcon', ['Player'])

        # Adding M2M table for field friends on 'Player'
        m2m_table_name = db.shorten_name('galcon_player_friends')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_player', models.ForeignKey(orm['galcon.player'], null=False)),
            ('to_player', models.ForeignKey(orm['galcon.player'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_player_id', 'to_player_id'])

        # Adding M2M table for field groups on 'Player'
        m2m_table_name = db.shorten_name('galcon_player_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('player', models.ForeignKey(orm['galcon.player'], null=False)),
            ('group', models.ForeignKey(orm['galcon.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['player_id', 'group_id'])

        # Adding M2M table for field trophies on 'Player'
        m2m_table_name = db.shorten_name('galcon_player_trophies')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('player', models.ForeignKey(orm['galcon.player'], null=False)),
            ('trophy', models.ForeignKey(orm['galcon.trophy'], null=False))
        ))
        db.create_unique(m2m_table_name, ['player_id', 'trophy_id'])

        # Adding model 'Group'
        db.create_table('galcon_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=65000)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('join_requires_approval', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('galcon', ['Group'])

        # Adding M2M table for field admins on 'Group'
        m2m_table_name = db.shorten_name('galcon_group_admins')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['galcon.group'], null=False)),
            ('player', models.ForeignKey(orm['galcon.player'], null=False))
        ))
        db.create_unique(m2m_table_name, ['group_id', 'player_id'])

        # Adding model 'Section'
        db.create_table('galcon_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('galcon', ['Section'])

        # Adding model 'Note'
        db.create_table('galcon_note', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=100)),
        ))
        db.send_create_signal('galcon', ['Note'])

        # Adding model 'Subsection'
        db.create_table('galcon_subsection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', to=orm['galcon.Section'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('galcon', ['Subsection'])

        # Adding model 'Thread'
        db.create_table('galcon_thread', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='threads', to=orm['galcon.Player'])),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', to=orm['galcon.Subsection'])),
            ('close_note', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['galcon.Note'], null=True, blank=True)),
            ('sticky', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('page_views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('galcon', ['Thread'])

        # Adding model 'Pm'
        db.create_table('galcon_pm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='messages', to=orm['galcon.Player'])),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=65000)),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('starred', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('galcon', ['Pm'])

        # Adding model 'Post'
        db.create_table('galcon_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['galcon.Player'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', to=orm['galcon.Thread'])),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('last_modification_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=65000)),
            ('flag_note', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['galcon.Note'], null=True, blank=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('galcon', ['Post'])

        # Adding model 'Friend_Request'
        db.create_table('galcon_friend_request', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_friend_requests', to=orm['galcon.Player'])),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='friend_requests', to=orm['galcon.Player'])),
            ('accepted', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('galcon', ['Friend_Request'])

        # Adding model 'Join_Group_Request'
        db.create_table('galcon_join_group_request', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_group_requests', to=orm['galcon.Player'])),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='membership_requests', to=orm['galcon.Group'])),
            ('accepted', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('galcon', ['Join_Group_Request'])

        # Adding model 'Trophy'
        db.create_table('galcon_trophy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=100)),
        ))
        db.send_create_signal('galcon', ['Trophy'])


    def backwards(self, orm):
        # Deleting model 'Rank'
        db.delete_table('galcon_rank')

        # Deleting model 'Player'
        db.delete_table('galcon_player')

        # Removing M2M table for field friends on 'Player'
        db.delete_table(db.shorten_name('galcon_player_friends'))

        # Removing M2M table for field groups on 'Player'
        db.delete_table(db.shorten_name('galcon_player_groups'))

        # Removing M2M table for field trophies on 'Player'
        db.delete_table(db.shorten_name('galcon_player_trophies'))

        # Deleting model 'Group'
        db.delete_table('galcon_group')

        # Removing M2M table for field admins on 'Group'
        db.delete_table(db.shorten_name('galcon_group_admins'))

        # Deleting model 'Section'
        db.delete_table('galcon_section')

        # Deleting model 'Note'
        db.delete_table('galcon_note')

        # Deleting model 'Subsection'
        db.delete_table('galcon_subsection')

        # Deleting model 'Thread'
        db.delete_table('galcon_thread')

        # Deleting model 'Pm'
        db.delete_table('galcon_pm')

        # Deleting model 'Post'
        db.delete_table('galcon_post')

        # Deleting model 'Friend_Request'
        db.delete_table('galcon_friend_request')

        # Deleting model 'Join_Group_Request'
        db.delete_table('galcon_join_group_request')

        # Deleting model 'Trophy'
        db.delete_table('galcon_trophy')


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
        'galcon.friend_request': {
            'Meta': {'object_name': 'Friend_Request'},
            'accepted': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_friend_requests'", 'to': "orm['galcon.Player']"}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friend_requests'", 'to': "orm['galcon.Player']"})
        },
        'galcon.group': {
            'Meta': {'object_name': 'Group'},
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'admined_groups'", 'to': "orm['galcon.Player']"}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '65000'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_requires_approval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'})
        },
        'galcon.join_group_request': {
            'Meta': {'object_name': 'Join_Group_Request'},
            'accepted': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_group_requests'", 'to': "orm['galcon.Player']"}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'membership_requests'", 'to': "orm['galcon.Group']"})
        },
        'galcon.note': {
            'Meta': {'object_name': 'Note'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        },
        'galcon.player': {
            'Meta': {'object_name': 'Player'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'friends_rel_+'", 'blank': 'True', 'to': "orm['galcon.Player']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'groups'", 'blank': 'True', 'to': "orm['galcon.Group']"}),
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
        'galcon.pm': {
            'Meta': {'object_name': 'Pm'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messages'", 'to': "orm['galcon.Player']"}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'}),
            'starred': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '65000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'galcon.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['galcon.Player']"}),
            'flag_note': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['galcon.Note']", 'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modification_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'to': "orm['galcon.Thread']"}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '65000'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        },
        'galcon.rank': {
            'Meta': {'object_name': 'Rank'},
            'classic_rank': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'flash_rank': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fusion_rank': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iphone_rank': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'galcon.section': {
            'Meta': {'object_name': 'Section'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        },
        'galcon.subsection': {
            'Meta': {'object_name': 'Subsection'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'to': "orm['galcon.Section']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        },
        'galcon.thread': {
            'Meta': {'object_name': 'Thread'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'threads'", 'to': "orm['galcon.Player']"}),
            'close_note': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['galcon.Note']", 'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'to': "orm['galcon.Subsection']"}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'galcon.trophy': {
            'Meta': {'object_name': 'Trophy'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['galcon']