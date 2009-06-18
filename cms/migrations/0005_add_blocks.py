
from south.db import db
from django.db import models
from cms.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Block'
        db.create_table('cms_block', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=255)),
            ('content', models.TextField(null=True, blank=True)),
            ('page', models.ForeignKey(orm.Page, related_name='blocks')),
        ))
        db.send_create_signal('cms', ['Block'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Block'
        db.delete_table('cms_block')
        
    
    
    models = {
        'cms.block': {
            'content': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'}),
            'page': ('models.ForeignKey', ["orm['cms.Page']"], {'related_name': "'blocks'"})
        },
        'cms.page': {
            'content': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'parent': ('models.ForeignKey', ["orm['cms.Page']"], {'related_name': "'children'", 'null': 'True', 'blank': 'True'}),
            'published': ('models.BooleanField', [], {'default': 'False'}),
            'slug': ('models.CharField', [], {'unique': 'True', 'max_length': '255', 'null': 'True'}),
            'template': ('models.CharField', [], {'max_length': '255', 'null': 'True'}),
            'title': ('models.CharField', [], {'max_length': '255'})
        },
        'cms.image': {
            'caption': ('models.TextField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('models.ImageField', [], {}),
            'name': ('models.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }
    
    complete_apps = ['cms']
