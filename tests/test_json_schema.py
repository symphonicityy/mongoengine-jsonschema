from enum import Enum
import pytest
from importlib.metadata import version

import mongoengine as me
from mongoengine_jsonschema import JsonSchemaMixin
import mongomock
from jsonschema import validate
from jsonschema.exceptions import ValidationError


class ChoiceEnum(Enum):
    A = '1'
    B = '2'
    C = '3'


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


class ExampleDocumentWithCustomSchema(me.Document, JsonSchemaMixin):
    _JSONSCHEMA = {
        '$id': '/schemas/ExampleDocumentWithCustomSchema',
        'type': 'object',
        'title': 'Example Document With Custom Schema',
        'properties': {},
        'additionalProperties': False
    }


class ExampleDocument(me.Document, JsonSchemaMixin):
    binary_field = me.BinaryField()
    boolean_field = me.BooleanField(required=True)
    cached_reference_field = me.CachedReferenceField(ExampleReferencedDocument)
    complex_datetime_field = me.ComplexDateTimeField()
    datetime_field = me.DateTimeField()
    date_field = me.DateField()
    decimal_field = me.DecimalField()
    dict_field = me.DictField()
    dynamic_field = me.DynamicField(default=1)
    email_field = me.EmailField()
    embedded_document_field = me.EmbeddedDocumentField(ExampleEmbeddedDocument)
    embedded_document_list_field = me.EmbeddedDocumentListField(ExampleEmbeddedDocument)
    enum_field = me.EnumField(ChoiceEnum)
    float_field = me.FloatField()
    generic_embedded_document_field = me.GenericEmbeddedDocumentField()
    generic_lazy_reference_field = me.GenericLazyReferenceField()
    generic_reference_field = me.GenericReferenceField()
    geo_point_field = me.GeoPointField()
    int_field = me.IntField(min_value=0, max_value=5)
    lazy_reference_field = me.LazyReferenceField(ExampleReferencedDocument)
    line_string_field = me.LineStringField()
    list_field = me.ListField(me.StringField(), required=True, default=['1'])
    long_field = me.LongField()
    map_field = me.MapField(me.IntField())
    multi_line_string_field = me.MultiLineStringField()
    multi_point_field = me.MultiPointField()
    multi_polygon_field = me.MultiPolygonField()
    object_ID_field = me.ObjectIdField()
    point_field = me.PointField(default=[0, 0])
    polygon_field = me.PolygonField()
    reference_field = me.ReferenceField(ExampleReferencedDocument)
    sequence_field = me.SequenceField()
    sorted_list_field = me.SortedListField(me.IntField())
    string_field = me.StringField(min_length=1, max_length=2, choices=['1', '2', '3'], regex=r'.*', default='1')
    string_field_excluded = me.StringField(exclude_from_schema=True)
    URL_field = me.URLField()
    UUID_field = me.UUIDField()


@pytest.fixture
def example_schema():
    return ExampleDocument.json_schema()


@pytest.fixture
def example_json():
    return {
        'boolean_field': True,
        'datetime_field': '2018-11-13 20:20:39',
        'date_field': '2018-11-13',
        'decimal_field': 1.1,
        'dict_field': {'A': 1},
        'dynamic_field': 'example',
        'email_field': 'example@example.com',
        'embedded_document_field': {'embedded_field': 'A'},
        'embedded_document_list_field': [{'embedded_field': 'A'}],
        'enum_field': '1',
        'float_field': 1.1,
        'generic_embedded_document_field': {'embedded_field': 'A',
                                            '_cls': 'ExampleEmbeddedDocument'},
        'geo_point_field': [1, 2],
        'int_field': 1,
        'line_string_field': {'type': 'LineString',
                              'coordinates': [[1, 2], [3, 4], [5, 6], [1, 2]]},
        'list_field': ['1', '2'],
        'long_field': 1,
        'map_field': {'A': 1},
        'multi_line_string_field': {'type': 'MultiLineString',
                                    'coordinates': [[[1, 2], [3, 4], [5, 6], [1, 2]],
                                                    [[7, 8], [9, 10], [11, 12], [7, 8]]]},
        'multi_point_field': [[1, 2], [3, 4]],
        'multi_polygon_field': [[[[1, 2], [3, 4], [5, 6], [1, 2]],
                                 [[7, 8], [9, 10], [11, 12], [7, 8]]],
                                [[[1, 2], [3, 4], [5, 6], [1, 2]],
                                 [[7, 8], [9, 10], [11, 12], [7, 8]]]
                                ],
        'object_ID_field': '507f191e810c19729de860ea',
        'point_field': {'type': 'Point',
                        'coordinates': [1, 2]},
        'polygon_field': {'type': 'Polygon',
                          'coordinates': [[[1, 2], [3, 4], [5, 6], [1, 2]],
                                          [[7, 8], [9, 10], [11, 12], [7, 8]]]},
        'sequence_field': 1,
        'sorted_list_field': [1, 2, 3],
        'string_field': '1',
        'URL_field': 'https://localhost:5000/api/',
        'UUID_field': '3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a'
    }


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

    def test_strict(self):
        schema = ExampleDocument.json_schema()
        assert 'required' in schema.keys()
        assert schema['required'] == ['boolean_field']

    def test_not_strict(self):
        schema = ExampleDocument.json_schema(strict=False)
        assert 'required' not in schema.keys()

    def test_custom_schema(self):
        schema = ExampleDocumentWithCustomSchema.json_schema()
        assert schema == {
            '$id': '/schemas/ExampleDocumentWithCustomSchema',
            'type': 'object',
            'title': 'Example Document With Custom Schema',
            'properties': {},
            'additionalProperties': False
        }


class TestDocumentSchemaProps:
    def test_binary_field(self, example_schema):
        assert example_schema['properties']['binary_field']['type'] == 'string'

    def test_cached_reference_field(self, example_schema):
        assert example_schema['properties']['cached_reference_field']['type'] == 'string'

    def test_date_field(self, example_schema):
        assert example_schema['properties']['date_field']['type'] == 'string'
        assert example_schema['properties']['date_field']['format'] == 'date'

    def test_embedded_document_list_field(self, example_schema):
        assert example_schema['properties']['embedded_document_list_field'] == {
            'type': 'array',
            'title': 'Embedded Document List Field',
            'items': {
                '$id': '/schemas/ExampleEmbeddedDocument',
                'title': 'Example Embedded Document',
                'additionalProperties': False,
                'type': 'object',
                'properties': {
                    'embedded_field': {
                        'title': 'Embedded Field',
                        'type': 'string'
                    }
                }
            }
        }

    def test_enum_field(self, example_schema):
        assert example_schema['properties']['enum_field']['type'] == 'string'
        assert example_schema['properties']['enum_field']['enum'] == ['1', '2', '3']

    def test_generic_lazy_reference_field(self, example_schema):
        assert example_schema['properties']['generic_lazy_reference_field']['type'] == 'string'

    def test_lazy_reference_field(self, example_schema):
        assert example_schema['properties']['lazy_reference_field']['type'] == 'string'

    def test_line_string_field(self, example_schema):
        assert example_schema['properties']['line_string_field'] == {
            'anyOf': [
                {
                    'type': 'object',
                    'title': 'Line String Field',
                    'properties': {
                        'type': {
                            'type': 'string',
                            'enum': ['LineString']
                        },
                        'coordinates': {
                            'type': 'array',
                            'items': {
                                'type': 'array',
                                'prefixItems': [
                                    {
                                        'type': 'number',  # longitude
                                        'min_value': -180,
                                        'max_value': 180
                                    },
                                    {
                                        'type': 'number',  # latitude
                                        'min_value': -90,
                                        'max_value': 90
                                    }
                                ],
                                'items': False
                            }
                        }
                    }
                },
                {
                    'type': 'array',
                    'title': 'Line String Field',
                    'items': {
                        'type': 'array',
                        'prefixItems': [
                            {
                                'type': 'number',  # longitude
                                'min_value': -180,
                                'max_value': 180
                            },
                            {
                                'type': 'number',  # latitude
                                'min_value': -90,
                                'max_value': 90
                            }
                        ],
                        'items': False
                    }
                }
            ]
        }

    def test_long_field(self, example_schema):
        assert example_schema['properties']['long_field']['type'] == 'integer'

    def test_multi_line_string_field(self, example_schema):
        assert example_schema['properties']['multi_line_string_field'] == {
            'anyOf': [
                {
                    'type': 'object',
                    'title': 'Multi Line String Field',
                    'properties': {
                        'type': {
                            'type': 'string',
                            'enum': ['MultiLineString']
                        },
                        'coordinates': {
                            'type': 'array',
                            'items': {
                                'type': 'array',
                                'items': {
                                    'type': 'array',
                                    'prefixItems': [
                                        {
                                            'type': 'number',  # longitude
                                            'min_value': -180,
                                            'max_value': 180
                                        },
                                        {
                                            'type': 'number',  # latitude
                                            'min_value': -90,
                                            'max_value': 90
                                        }
                                    ],
                                    'items': False
                                }
                            }
                        }
                    }
                },
                {
                    'type': 'array',
                    'title': 'Multi Line String Field',
                    'items': {
                        'type': 'array',
                        'items': {
                            'type': 'array',
                            'prefixItems': [
                                {
                                    'type': 'number',  # longitude
                                    'min_value': -180,
                                    'max_value': 180
                                },
                                {
                                    'type': 'number',  # latitude
                                    'min_value': -90,
                                    'max_value': 90
                                }
                            ],
                            'items': False
                        }
                    }
                }
            ]
        }

    def test_multi_point_field(self, example_schema):
        assert example_schema['properties']['multi_point_field'] == {
            'anyOf': [
                {
                    'type': 'object',
                    'title': 'Multi Point Field',
                    'properties': {
                        'type': {
                            'type': 'string',
                            'enum': ['MultiPoint']
                        },
                        'coordinates': {
                            'type': 'array',
                            'items': {
                                'type': 'array',
                                'prefixItems': [
                                    {
                                        'type': 'number',  # longitude
                                        'min_value': -180,
                                        'max_value': 180
                                    },
                                    {
                                        'type': 'number',  # latitude
                                        'min_value': -90,
                                        'max_value': 90
                                    }
                                ],
                                'items': False
                            }
                        }
                    }
                },
                {
                    'type': 'array',
                    'title': 'Multi Point Field',
                    'items': {
                        'type': 'array',
                        'prefixItems': [
                            {
                                'type': 'number',  # longitude
                                'min_value': -180,
                                'max_value': 180
                            },
                            {
                                'type': 'number',  # latitude
                                'min_value': -90,
                                'max_value': 90
                            }
                        ],
                        'items': False
                    }
                }
            ]
        }

    def test_multi_polygon_field(self, example_schema):
        assert example_schema['properties']['multi_polygon_field'] == {
            'anyOf': [
                {
                    'type': 'object',
                    'title': 'Multi Polygon Field',
                    'properties': {
                        'type': {
                            'type': 'string',
                            'enum': ['MultiPolygon']
                        },
                        'coordinates': {
                            'type': 'array',
                            'items': {
                                'type': 'array',
                                'items': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'array',
                                        'prefixItems': [
                                            {
                                                'type': 'number',  # longitude
                                                'min_value': -180,
                                                'max_value': 180
                                            },
                                            {
                                                'type': 'number',  # latitude
                                                'min_value': -90,
                                                'max_value': 90
                                            }
                                        ],
                                        'items': False
                                    }
                                }
                            }
                        }
                    }
                },
                {
                    'type': 'array',
                    'title': 'Multi Polygon Field',
                    'items': {
                        'type': 'array',
                        'items': {
                            'type': 'array',
                            'items': {
                                'type': 'array',
                                'prefixItems': [
                                    {
                                        'type': 'number',  # longitude
                                        'min_value': -180,
                                        'max_value': 180
                                    },
                                    {
                                        'type': 'number',  # latitude
                                        'min_value': -90,
                                        'max_value': 90
                                    }
                                ],
                                'items': False
                            }
                        }
                    }
                }
            ]
        }

    def test_point_field(self, example_schema):
        assert example_schema['properties']['point_field'] == {
            'anyOf': [
                {
                    'type': 'object',
                    'title': 'Point Field',
                    'properties': {
                        'type': {
                            'type': 'string',
                            'enum': ['Point']
                        },
                        'coordinates': {
                            'type': 'array',
                            'prefixItems': [
                                {
                                    'type': 'number',  # longitude
                                    'min_value': -180,
                                    'max_value': 180
                                },
                                {
                                    'type': 'number',  # latitude
                                    'min_value': -90,
                                    'max_value': 90
                                }
                            ],
                            'items': False
                        }
                    }
                },
                {
                    'type': 'array',
                    'title': 'Point Field',
                    'prefixItems': [
                        {
                            'type': 'number',  # longitude
                            'min_value': -180,
                            'max_value': 180
                        },
                        {
                            'type': 'number',  # latitude
                            'min_value': -90,
                            'max_value': 90
                        }
                    ],
                    'items': False
                }
            ]
        }

    def test_polygon_field(self, example_schema):
        assert example_schema['properties']['polygon_field'] == {
            'anyOf': [
                {
                    'type': 'object',
                    'title': 'Polygon Field',
                    'properties': {
                        'type': {
                            'type': 'string',
                            'enum': ['Polygon']
                        },
                        'coordinates': {
                            'type': 'array',
                            'items': {
                                'type': 'array',
                                'items': {
                                    'type': 'array',
                                    'prefixItems': [
                                        {
                                            'type': 'number',  # longitude
                                            'min_value': -180,
                                            'max_value': 180
                                        },
                                        {
                                            'type': 'number',  # latitude
                                            'min_value': -90,
                                            'max_value': 90
                                        }
                                    ],
                                    'items': False
                                }
                            }
                        }
                    }
                },
                {
                    'type': 'array',
                    'title': 'Polygon Field',
                    'items': {
                        'type': 'array',
                        'items': {
                            'type': 'array',
                            'prefixItems': [
                                {
                                    'type': 'number',  # longitude
                                    'min_value': -180,
                                    'max_value': 180
                                },
                                {
                                    'type': 'number',  # latitude
                                    'min_value': -90,
                                    'max_value': 90
                                }
                            ],
                            'items': False
                        }
                    }
                }
            ]
        }

    def test_string_field(self, example_schema):
        assert 'string_field' in example_schema['properties'].keys()
        assert example_schema['properties']['string_field']['type'] == 'string'

    def test_string_field_excluded(self, example_schema):
        assert 'string_field_excluded' not in example_schema['properties'].keys()

    def test_int_field(self, example_schema):
        assert 'int_field' in example_schema['properties'].keys()
        assert example_schema['properties']['int_field']['type'] == 'integer'

    def test_float_field(self, example_schema):
        assert 'float_field' in example_schema['properties'].keys()
        assert example_schema['properties']['float_field']['type'] == 'number'

    def test_boolean_field(self, example_schema):
        assert 'boolean_field' in example_schema['properties'].keys()
        assert example_schema['properties']['boolean_field']['type'] == 'boolean'

    def test_datetime_field(self, example_schema):
        assert 'datetime_field' in example_schema['properties'].keys()
        assert example_schema['properties']['datetime_field']['type'] == 'string'
        assert example_schema['properties']['datetime_field']['format'] == 'date-time'

    def test_embedded_document_field(self, example_schema):
        assert 'embedded_document_field' in example_schema['properties'].keys()
        assert example_schema['properties']['embedded_document_field']['type'] == 'object'

    def test_list_field(self, example_schema):
        assert 'list_field' in example_schema['properties'].keys()
        assert example_schema['properties']['list_field']['type'] == 'array'

    def test_dict_field(self, example_schema):
        assert 'dict_field' in example_schema['properties'].keys()
        assert example_schema['properties']['dict_field']['type'] == 'object'

    def test_objectid_field(self, example_schema):
        assert 'object_ID_field' in example_schema['properties'].keys()
        assert example_schema['properties']['object_ID_field']['type'] == 'string'

    def test_reference_field(self, example_schema):
        assert 'reference_field' in example_schema['properties'].keys()
        assert example_schema['properties']['reference_field']['type'] == 'string'

    def test_map_field(self, example_schema):
        assert 'map_field' in example_schema['properties'].keys()
        assert example_schema['properties']['map_field']['type'] == 'object'
        assert example_schema['properties']['map_field']['patternProperties'] == {'.*': {'type': 'integer'}}

    def test_decimal_field(self, example_schema):
        assert 'decimal_field' in example_schema['properties'].keys()
        assert example_schema['properties']['decimal_field']['type'] == 'number'

    def test_complex_datetime_field(self, example_schema):
        assert 'complex_datetime_field' in example_schema['properties'].keys()
        assert example_schema['properties']['complex_datetime_field']['type'] == 'string'
        assert example_schema['properties']['complex_datetime_field']['format'] == 'date-time'

    def test_url_field(self, example_schema):
        assert 'URL_field' in example_schema['properties'].keys()
        assert example_schema['properties']['URL_field']['type'] == 'string'
        assert example_schema['properties']['URL_field']['format'] == 'uri'
        assert example_schema['properties']['URL_field'][
                   'pattern'] == '^(?:[a-z0-9\\.\\-]*)://(?:(?:[A-Z0-9](?:[A-Z0-9-_]{0,61}[A-Z0-9])?\\.)+(?:[A-Z]{2,6}\\.?|[A-Z0-9-]{2,}(?<!-)\\.?)|localhost|\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}|\\[?[A-F0-9]*:[A-F0-9:]+\\]?)(?::\\d+)?(?:/?|[/?]\\S+)$'

    def test_dynamic_field(self, example_schema):
        assert 'dynamic_field' in example_schema['properties'].keys()
        assert example_schema['properties']['dynamic_field'] == {'default': 1, 'title': 'Dynamic Field'}

    def test_generic_reference_field(self, example_schema):
        assert 'generic_reference_field' in example_schema['properties'].keys()
        assert example_schema['properties']['generic_reference_field']['type'] == 'string'

    def test_sorted_list_field(self, example_schema):
        assert 'sorted_list_field' in example_schema['properties'].keys()
        assert example_schema['properties']['sorted_list_field']['type'] == 'array'

    def test_email_field(self, example_schema):
        assert 'email_field' in example_schema['properties'].keys()
        assert example_schema['properties']['email_field']['type'] == 'string'
        assert example_schema['properties']['email_field']['format'] == 'email'

    def test_geo_point_field(self, example_schema):
        assert 'geo_point_field' in example_schema['properties'].keys()
        assert example_schema['properties']['geo_point_field'] == {
            'type': 'array',
            'title': 'Geo Point Field',
            'prefixItems': [
                {
                    'type': 'number',  # longitude
                    'min_value': -180,
                    'max_value': 180
                },
                {
                    'type': 'number',  # latitude
                    'min_value': -90,
                    'max_value': 90
                }
            ],
            'items': False
        }

    def test_sequence_field(self, example_schema):
        assert 'sequence_field' in example_schema['properties'].keys()
        assert example_schema['properties']['sequence_field']['type'] == 'integer'

    def test_uuid_field(self, example_schema):
        assert 'UUID_field' in example_schema['properties'].keys()
        assert example_schema['properties']['UUID_field']['type'] == 'string'
        assert example_schema['properties']['UUID_field']['format'] == 'uuid'

    def test_generic_embedded_document_field(self, example_schema):
        assert 'generic_embedded_document_field' in example_schema['properties'].keys()
        assert example_schema['properties']['generic_embedded_document_field'] == {
            'type': 'object',
            'title': 'Generic Embedded Document Field'
        }


class TestDocumentSchemaArgs:
    def test_default(self, example_schema):
        assert example_schema['properties']['string_field']['default'] == '1'

    def test_min_length(self, example_schema):
        assert example_schema['properties']['string_field']['minLength'] == 1

    def test_max_length(self, example_schema):
        assert example_schema['properties']['string_field']['maxLength'] == 2

    def test_min_value(self, example_schema):
        assert example_schema['properties']['int_field']['minimum'] == 0

    def test_max_value(self, example_schema):
        assert example_schema['properties']['int_field']['maximum'] == 5

    def test_choices(self, example_schema):
        assert example_schema['properties']['string_field']['enum'] == ['1', '2', '3']

    def test_regex(self, example_schema):
        assert example_schema['properties']['string_field']['pattern'] == '.*'

    def test_list_required(self, example_schema):
        assert example_schema['properties']['list_field']['minItems'] == 1

    def test_list_items(self, example_schema):
        assert 'items' in example_schema['properties']['list_field'].keys()
        assert example_schema['properties']['list_field']['items'] == {'type': 'string'}


class TestTitle:
    def test_field_title(self, example_schema):
        assert example_schema['properties']['object_ID_field']['title'] == 'Object ID Field'
        assert example_schema['properties']['UUID_field']['title'] == 'UUID Field'
        assert example_schema['properties']['string_field']['title'] == 'String Field'

    def test_document_title(self, example_schema):
        assert example_schema['title'] == 'Example Document'


class TestValidation:
    def test_jsonschema_validation(self, example_json, example_schema):
        try:
            validate(example_json, example_schema)
        except ValidationError as e:
            assert False, f"JSON schema validation failed. {str(e)}"

    def test_mongoengine_validation(self, example_json):
        me_version = version('mongoengine')
        if me_version < '0.27.0':
            me.connect('mongoenginetest', host='mongomock://localhost', alias='default')
        else:
            me.connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient,
                       alias='default')
        conn = me.get_connection('default')
        try:
            ExampleDocument(**example_json).validate()
        except me.ValidationError as e:
            assert False, f"Mongoengine validation failed. {str(e)}"
