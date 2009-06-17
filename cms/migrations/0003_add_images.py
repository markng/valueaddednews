
from south.db import db
from django.db import models
from cms.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Image'
        db.create_table('cms_image', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(unique=True, max_length=255)),
            ('caption', models.TextField()),
            ('image', models.ImageField()),
        ))
        db.send_create_signal('cms', ['Image'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Image'
        db.delete_table('cms_image')
        
    
    
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
            'title': ('models.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['cms']
