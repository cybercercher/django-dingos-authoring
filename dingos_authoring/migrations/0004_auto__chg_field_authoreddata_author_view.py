# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AuthoredData.author_view'
        db.alter_column(u'dingos_authoring_authoreddata', 'author_view_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dingos_authoring.AuthorView'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'AuthoredData.author_view'
        raise RuntimeError("Cannot reverse this migration. 'AuthoredData.author_view' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'AuthoredData.author_view'
        db.alter_column(u'dingos_authoring_authoreddata', 'author_view_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dingos_authoring.AuthorView']))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dingos.datatypenamespace': {
            'Meta': {'object_name': 'DataTypeNameSpace'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'dingos.fact': {
            'Meta': {'object_name': 'Fact'},
            'fact_term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dingos.FactTerm']"}),
            'fact_values': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dingos.FactValue']", 'null': 'True', 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value_iobject_id': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'value_of_set'", 'null': 'True', 'to': u"orm['dingos.Identifier']"}),
            'value_iobject_ts': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'dingos.factdatatype': {
            'Meta': {'unique_together': "(('name', 'namespace'),)", 'object_name': 'FactDataType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'namespace': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fact_data_type_set'", 'to': u"orm['dingos.DataTypeNameSpace']"})
        },
        u'dingos.factterm': {
            'Meta': {'unique_together': "(('term', 'attribute'),)", 'object_name': 'FactTerm'},
            'attribute': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'dingos.facttermnamespacemap': {
            'Meta': {'object_name': 'FactTermNamespaceMap'},
            'fact_term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dingos.FactTerm']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'namespaces': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dingos.DataTypeNameSpace']", 'through': u"orm['dingos.PositionalNamespace']", 'symmetrical': 'False'})
        },
        u'dingos.factvalue': {
            'Meta': {'unique_together': "(('value', 'fact_data_type', 'storage_location'),)", 'object_name': 'FactValue'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fact_data_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fact_value_set'", 'to': u"orm['dingos.FactDataType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'storage_location': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'dingos.identifier': {
            'Meta': {'unique_together': "(('uid', 'namespace'),)", 'object_name': 'Identifier'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'latest_of'", 'unique': 'True', 'null': 'True', 'to': u"orm['dingos.InfoObject']"}),
            'namespace': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dingos.IdentifierNameSpace']"}),
            'uid': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'dingos.identifiernamespace': {
            'Meta': {'object_name': 'IdentifierNameSpace'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_substitution': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'dingos.infoobject': {
            'Meta': {'ordering': "['-timestamp']", 'unique_together': "(('identifier', 'timestamp'),)", 'object_name': 'InfoObject'},
            'create_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'facts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dingos.Fact']", 'through': u"orm['dingos.InfoObject2Fact']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'iobject_set'", 'to': u"orm['dingos.Identifier']"}),
            'iobject_family': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'iobject_set'", 'to': u"orm['dingos.InfoObjectFamily']"}),
            'iobject_family_revision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['dingos.Revision']"}),
            'iobject_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'iobject_set'", 'to': u"orm['dingos.InfoObjectType']"}),
            'iobject_type_revision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['dingos.Revision']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Unnamed'", 'max_length': '255', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'dingos.infoobject2fact': {
            'Meta': {'ordering': "['node_id__name']", 'object_name': 'InfoObject2Fact'},
            'attributed_fact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attributes'", 'null': 'True', 'to': u"orm['dingos.InfoObject2Fact']"}),
            'fact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'iobject_thru'", 'to': u"orm['dingos.Fact']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iobject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fact_thru'", 'to': u"orm['dingos.InfoObject']"}),
            'namespace_map': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dingos.FactTermNamespaceMap']", 'null': 'True'}),
            'node_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dingos.NodeID']"})
        },
        u'dingos.infoobjectfamily': {
            'Meta': {'object_name': 'InfoObjectFamily'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '256'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'})
        },
        u'dingos.infoobjecttype': {
            'Meta': {'unique_together': "(('name', 'iobject_family', 'namespace'),)", 'object_name': 'InfoObjectType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iobject_family': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'iobject_type_set'", 'to': u"orm['dingos.InfoObjectFamily']"}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '30'}),
            'namespace': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'iobject_type_set'", 'blank': 'True', 'to': u"orm['dingos.DataTypeNameSpace']"})
        },
        u'dingos.nodeid': {
            'Meta': {'object_name': 'NodeID'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'dingos.positionalnamespace': {
            'Meta': {'object_name': 'PositionalNamespace'},
            'fact_term_namespace_map': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'namespaces_thru'", 'to': u"orm['dingos.FactTermNamespaceMap']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'namespace': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fact_term_namespace_map_thru'", 'to': u"orm['dingos.DataTypeNameSpace']"}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'dingos.revision': {
            'Meta': {'object_name': 'Revision'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        u'dingos_authoring.authoreddata': {
            'Meta': {'unique_together': "(('group', 'user', 'identifier', 'kind', 'timestamp'),)", 'object_name': 'AuthoredData'},
            'author_view': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dingos_authoring.AuthorView']", 'null': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dingos_authoring.Identifier']"}),
            'kind': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'processing_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'dingos_authoring.authorview': {
            'Meta': {'object_name': 'AuthorView'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'dingos_authoring.groupnamespacemap': {
            'Meta': {'object_name': 'GroupNamespaceMap'},
            'allowed_namespaces': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'authoring_allowed_for'", 'blank': 'True', 'to': u"orm['dingos.IdentifierNameSpace']"}),
            'default_namespace': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'authoring_default_for'", 'to': u"orm['dingos.IdentifierNameSpace']"}),
            'group': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.Group']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dingos_authoring.identifier': {
            'Meta': {'object_name': 'Identifier'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'dingos_authoring.infoobject2authoreddata': {
            'Meta': {'object_name': 'InfoObject2AuthoredData'},
            'authored_data': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['dingos_authoring.AuthoredData']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iobject': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'created_from_thru'", 'unique': 'True', 'to': u"orm['dingos.InfoObject']"})
        }
    }

    complete_apps = ['dingos_authoring']