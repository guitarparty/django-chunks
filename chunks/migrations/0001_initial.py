# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Chunk'
        db.create_table('chunks_chunk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('lang_code', self.gf('django.db.models.fields.CharField')(default='is', max_length=5, blank=True)),
        ))
        db.send_create_signal('chunks', ['Chunk'])


    def backwards(self, orm):
        
        # Deleting model 'Chunk'
        db.delete_table('chunks_chunk')


    models = {
        'chunks.chunk': {
            'Meta': {'object_name': 'Chunk'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lang_code': ('django.db.models.fields.CharField', [], {'default': "'is'", 'max_length': '5', 'blank': 'True'})
        }
    }

    complete_apps = ['chunks']
