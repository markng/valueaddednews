
from south.db import db
from django.db import models
from cms.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Page.template'
        db.add_column('cms_page', 'template', models.CharField(max_length=255, null=True))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Page.template'
        db.delete_column('cms_page', 'template')
        
    
    
    models = {
        'cms.image': {
            'caption': ('models.TextField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('models.ImageField', [], {}),
            'name': ('models.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'cms.page': {
            'content': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'parent': ('models.ForeignKey', ["orm['cms.Page']"], {'related_name': "'children'", 'null': 'True', 'blank': 'True'}),
            'published': ('models.BooleanField', [], {'default': 'False'}),
            'slug': ('models.CharField', [], {'unique': 'True', 'max_length': '255', 'null': 'True'}),
            'template': ('models.CharField', [], {'max_length': '255', 'null': 'True'}),
            'title': ('models.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['cms']
