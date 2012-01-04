# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'HIT'
        db.create_table('djurk_hit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mturk_id', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True)),
            ('hit_type_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('keywords', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('reward', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=3, blank=True)),
            ('lifetime_in_seconds', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('assignment_duration_in_seconds', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('max_assignments', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, null=True, blank=True)),
            ('auto_approval_delay_in_seconds', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('requester_annotation', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('number_of_similar_hits', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('review_status', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('number_of_assignments_pending', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('number_of_assignments_available', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('number_of_assignments_completed', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='hit', null=True, to=orm['contenttypes.ContentType'])),
            ('content_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('djurk', ['HIT'])

        # Adding model 'Assignment'
        db.create_table('djurk_assignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mturk_id', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True)),
            ('worker_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('hit', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='assignments', null=True, to=orm['djurk.HIT'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('auto_approval_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('accept_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('submit_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('approval_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('rejection_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('requester_feedback', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('djurk', ['Assignment'])

        # Adding model 'KeyValue'
        db.create_table('djurk_keyvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='answers', null=True, to=orm['djurk.Assignment'])),
        ))
        db.send_create_signal('djurk', ['KeyValue'])


    def backwards(self, orm):
        
        # Deleting model 'HIT'
        db.delete_table('djurk_hit')

        # Deleting model 'Assignment'
        db.delete_table('djurk_assignment')

        # Deleting model 'KeyValue'
        db.delete_table('djurk_keyvalue')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'djurk.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'accept_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'approval_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'auto_approval_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assignments'", 'null': 'True', 'to': "orm['djurk.HIT']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mturk_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True'}),
            'rejection_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'requester_feedback': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'submit_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'worker_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'djurk.hit': {
            'Meta': {'object_name': 'HIT'},
            'assignment_duration_in_seconds': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'auto_approval_delay_in_seconds': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'hit'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hit_type_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'lifetime_in_seconds': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_assignments': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'mturk_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True'}),
            'number_of_assignments_available': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number_of_assignments_completed': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number_of_assignments_pending': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'number_of_similar_hits': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'requester_annotation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'review_status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'reward': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '3', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'djurk.keyvalue': {
            'Meta': {'object_name': 'KeyValue'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'answers'", 'null': 'True', 'to': "orm['djurk.Assignment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['djurk']
