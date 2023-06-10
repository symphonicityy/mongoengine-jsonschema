import pytest
from bson import ObjectId
import uuid
import datetime as dt
import mongoengine as me
from mongoengine_jsonschema import JsonSchemaMixin


class ExampleBaseNoMixinDocument(me.Document):
    meta = {'allow_inheritance': True}
    base_field_not_in_schema = me.StringField()


class ExampleBaseDocument(me.Document, JsonSchemaMixin):
    meta = {'allow_inheritance': True}
    base_field = me.StringField()


class ExampleEmbeddedDocument(me.EmbeddedDocument, JsonSchemaMixin):
    embedded_field = me.StringField()


class ExampleDynamicEmbeddedDocument(me.DynamicEmbeddedDocument, JsonSchemaMixin):
    embedded_field = me.StringField()
    multi_embedded_field = me.EmbeddedDocumentField(ExampleEmbeddedDocument)


class ExampleDynamicDocument(me.DynamicDocument, JsonSchemaMixin):
    field = me.StringField()


class ExampleReferencedDocument(me.Document, JsonSchemaMixin):
    pass


class ExampleDocumentInherited(ExampleBaseDocument):
    field = me.StringField()


class ExampleDocumentInheritedNoMixinParent(ExampleBaseNoMixinDocument, JsonSchemaMixin):
    field = me.StringField()


class ExampleDocument(me.Document, JsonSchemaMixin):
    string_field = me.StringField(default="1", min_length=1, max_length=2, choices=["1", "2", "3"], regex=r".*")
    string_field_excluded = me.StringField(exclude_from_schema=True)
    int_field = me.IntField(default=1, min_value=0, max_value=5)
    float_field = me.FloatField(default=1.1)
    boolean_field = me.BooleanField(default=True)
    datetime_field = me.DateTimeField(default=dt.datetime.now)
    embedded_document_field = me.EmbeddedDocumentField(ExampleEmbeddedDocument)
    list_field = me.ListField(me.EmbeddedDocumentField(ExampleEmbeddedDocument))
    dict_field = me.DictField(default=lambda: {"hello": "world"})
    objectid_field = me.ObjectIdField(default=ObjectId)
    reference_field = me.ReferenceField(ExampleReferencedDocument)
    map_field = me.MapField(me.IntField(), default=lambda: {"simple": 1})
    decimal_field = me.DecimalField(default=1.0)
    complex_datetime_field = me.ComplexDateTimeField(default=dt.datetime.now)
    url_field = me.URLField(default="http://mongoengine.org")
    dynamic_field = me.DynamicField(default=1)
    generic_reference_field = me.GenericReferenceField()
    sorted_list_field = me.SortedListField(me.IntField(), default=lambda: [1, 2, 3])
    email_field = me.EmailField(default="ross@example.com")
    geo_point_field = me.GeoPointField(default=lambda: [1, 2])
    sequence_field = me.SequenceField()
    uuid_field = me.UUIDField(default=uuid.uuid4)
    generic_embedded_document_field = me.GenericEmbeddedDocumentField()


@pytest.fixture
def schema():
    return ExampleDocument.json_schema()


class TestDocumentSchema:
    def test_base_doc(self):
        schema = ExampleBaseDocument.json_schema()
        assert isinstance(schema, dict)
        assert 'base_field' in schema['properties'].keys()
        assert schema['properties']['base_field']['type'] == 'string'

    def test_inherited_doc(self):
        schema = ExampleDocumentInherited.json_schema()
        assert isinstance(schema, dict)
        assert 'base_field' in schema['properties'].keys()
        assert 'field' in schema['properties'].keys()
        assert schema['properties']['base_field']['type'] == 'string'

    def test_inherited_no_mixin_parent_doc(self):
        schema = ExampleDocumentInheritedNoMixinParent.json_schema()
        assert isinstance(schema, dict)
        assert 'base_field_not_in_schema' not in schema['properties'].keys()

    def test_dynamic_doc(self):
        schema = ExampleDynamicDocument.json_schema()
        assert isinstance(schema, dict)
        assert 'additionalProperties' in schema.keys()
        assert schema['additionalProperties'] is True


class TestDocumentSchemaProps:
    def test_string_field(self, schema):
        assert 'string_field' in schema['properties'].keys()

    def test_string_field_excluded(self, schema):
        assert 'string_field_excluded' not in schema['properties'].keys()

    def test_int_field(self, schema):
        assert 'int_field' in schema['properties'].keys()

    def test_float_field(self, schema):
        assert 'float_field' in schema['properties'].keys()

    def test_boolean_field(self, schema):
        assert 'boolean_field' in schema['properties'].keys()

    def test_datetime_field(self, schema):
        assert 'datetime_field' in schema['properties'].keys()

    def test_embedded_document_field(self, schema):
        assert 'embedded_document_field' in schema['properties'].keys()

    def test_list_field(self, schema):
        assert 'list_field' in schema['properties'].keys()

    def test_dict_field(self, schema):
        assert 'dict_field' in schema['properties'].keys()

    def test_objectid_field(self, schema):
        assert 'objectid_field' in schema['properties'].keys()

    def test_reference_field(self, schema):
        assert 'reference_field' in schema['properties'].keys()

    def test_map_field(self, schema):
        assert 'map_field' in schema['properties'].keys()

    def test_decimal_field(self, schema):
        assert 'decimal_field' in schema['properties'].keys()

    def test_complex_datetime_field(self, schema):
        assert 'complex_datetime_field' in schema['properties'].keys()

    def test_url_field(self, schema):
        assert 'url_field' in schema['properties'].keys()

    def test_dynamic_field(self, schema):
        assert 'dynamic_field' in schema['properties'].keys()

    def test_generic_reference_field(self, schema):
        assert 'generic_reference_field' in schema['properties'].keys()

    def test_sorted_list_field(self, schema):
        assert 'sorted_list_field' in schema['properties'].keys()

    def test_email_field(self, schema):
        assert 'email_field' in schema['properties'].keys()

    def test_geo_point_field(self, schema):
        assert 'geo_point_field' in schema['properties'].keys()

    def test_sequence_field(self, schema):
        assert 'sequence_field' in schema['properties'].keys()

    def test_uuid_field(self, schema):
        assert 'uuid_field' in schema['properties'].keys()

    def test_generic_embedded_document_field(self, schema):
        assert 'generic_embedded_document_field' in schema['properties'].keys()


class TestDocumentSchemaArgs:
    pass


"""
fields
excluded fields
arguments
inherited fields
no mixin parent field exclusion
pascal case title
snake case title
strict
required
"""

