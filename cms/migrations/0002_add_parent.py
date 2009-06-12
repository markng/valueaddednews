
from south.db import db
from django.db import models
from cms.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Page.parent'
        db.add_column('cms_page', 'parent', models.ForeignKey(orm.Page, related_name='children', null=True, blank=True))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Page.parent'
        db.delete_column('cms_page', 'parent_id')
        
    
    
    models = {
        'cms.page': {
            'content': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'parent': ('models.ForeignKey', ["'self'"], {'related_name': "'children'", 'null': 'True', 'blank': 'True'}),
            'published': ('models.BooleanField', [], {'default': 'False'}),
            'slug': ('models.CharField', [], {'max_length': '255'}),
            'title': ('models.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['cms']
