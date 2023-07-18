import typing
import re

import mongoengine as me
import mongoengine.base


TYPE_MAP = {
    'BinaryField': 'string',
    'BooleanField': 'boolean',
    'CachedReferenceField': 'string',
    'ComplexDateTimeField': 'string',
    'DateField': 'string',
    'DateTimeField': 'string',
    'Decimal128Field': 'number',
    'DecimalField': 'number',
    'DictField': 'object',
    'EmailField': 'string',
    'EnumField': 'string',
    'FloatField': 'number',
    'GenericReferenceField': 'string',
    'GenericLazyReferenceField': 'string',
    'GeoPointField': 'array',
    'IntField': 'integer',
    'LongField': 'integer',
    'MapField': 'object',
    'ObjectIdField': 'string',
    'ReferenceField': 'string',
    'LazyReferenceField': 'string',
    'SequenceField': 'integer',
    'StringField': 'string',
    'URLField': 'string',
    'UUIDField': 'string',
}

ATTR_MAP = {'required': 'required',
            'default': 'default',
            'min_value': 'minimum',
            'max_value': 'maximum',
            'min_length': 'minLength',
            'max_length': 'maxLength',
            'choices': 'enum',
            'regex': 'pattern',
            'url_regex': 'pattern'}

POINT_PROP = {
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


class JsonSchemaMixin:
    """Mixin class that adds generating JSON schema functionality directly to MongoEngine documents."""

    _STRICT = False

    @classmethod
    def _get_title(cls, name: str) -> str:
        """
        Converts snake_case field names or PascalCase class names (assuming you follow PEP8 standards) to capitalized
        human-readable format. Used to set property title in schema.

        Args:
            name(str): Field or class name to convert

        Returns:
            str

        """

        if '_' in name or name.islower():
            name = name.split('_')
            name = list(map(lambda w: w.title() if w.islower() else w, name))
            return ' '.join(name)
        else:
            return ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', name))

    @classmethod
    def _add_title(cls, name: str, prop: dict) -> dict:
        """
        Returns property JSON with title.

        Args:
            name(str): Name given to field
            prop(dict): Generated property JSON

        Returns:
            dict
        """

        return {**prop, 'title': cls._get_title(name)}

    @classmethod
    def _parse_special_fields(cls, field: me.fields.BaseField) -> dict:
        """
        Returns field specific JSON schema keywords.

        Args:
            field(me.fields.BaseField): An instance of any MongoEngine base field.

        Returns:
            dict
        """

        if isinstance(field, me.fields.GeoPointField):
            return POINT_PROP

        elif isinstance(field, me.fields.UUIDField):
            return {'format': 'uuid'}

        elif isinstance(field, me.fields.EmailField):
            return {'format': 'email'}

        elif isinstance(field, me.fields.DateField):
            return {'format': 'date'}

        elif isinstance(field, (me.fields.DateTimeField, me.fields.ComplexDateTimeField)):
            return {'format': 'date-time'}

        elif isinstance(field, me.fields.URLField):
            return {'format': 'uri'}

        elif isinstance(field, me.fields.EnumField):
            _field = getattr(field, 'choices', None)
            return {'enum': [e.value for e in _field]}

        elif isinstance(field, me.fields.MapField):
            _field = getattr(field, 'field', None)
            _field_type = TYPE_MAP.get(type(_field).__name__, None)

            if None not in (_field, _field_type):
                return {'patternProperties': {
                    ".*": {"type": TYPE_MAP.get(type(_field).__name__, None)}
                }
                }

    @classmethod
    def _parse_field(cls, field: me.fields.BaseField) -> dict:
        """
        Generates property JSON by parsing MongoEngine field's arguments and returns it.
        
        Args:
            field(me.fields.BaseField): An instance of any MongoEngine base field.

        Returns:
            dict
        """
        _type = TYPE_MAP.get(type(field).__name__, None)
        field_dict = {'type': _type} if _type is not None else {}
        _parsed_special = cls._parse_special_fields(field)
        if _parsed_special is not None:
            field_dict = {**field_dict, **_parsed_special}

        for k, v in ATTR_MAP.items():
            _val = getattr(field, k, None)
            if isinstance(field, me.fields.EnumField) and k == 'choices':
                continue
            if _val is not None:
                field_dict[v] = _val

        if 'pattern' in field_dict.keys() and field_dict['pattern'] is not None:
            field_dict['pattern'] = field_dict['pattern'].pattern

        if 'default' in field_dict.keys() and isinstance(getattr(field, 'default'), typing.Callable):
            field_dict['default'] = [] if type(field) == me.fields.ListField else {}

        field_dict.pop('unique', None)
        return field_dict

    @classmethod
    def _parse_embedded_doc_field(cls, field: typing.Union[me.fields.EmbeddedDocumentField,
                                                           me.fields.GenericEmbeddedDocumentField] = None):
        """
        Generates JSON schema for given EmbeddedDocumentField and returns it. Make sure the embedded document
        class also inherits this mixin class (JsonSchemaMixin) or this method will return an empty dictionary.

        Args:
            field(typing.Union[me.fields.EmbeddedDocumentField, me.fields.GenericEmbeddedDocumentField]):
                A MongoEngine EmbeddedDocumentField instance

        Returns:
            dict
        """

        if field is None:
            return {}

        elif isinstance(field, me.fields.GenericEmbeddedDocumentField):
            return {
                'type': 'object'
            }

        try:
            return field.document_type_obj.json_schema(strict=cls._STRICT)
        except AttributeError:
            return {}

    @classmethod
    def _parse_geo_field(cls, field: me.base.GeoJsonBaseField = None) -> dict:
        """
        Returns JSON schema reference of given GeoJsonBaseField instance. All geo JSON fields can be defined in JSON
        as both arrays and objects, therefore schema is defined with 'anyOf' keyword.

        Args:
            field(me.base.GeoJsonBaseField): A MongoEngine GeoJsonBaseField instance

        Returns:
            dict
        """

        if field is None:
            return {}

        _coord_prop = POINT_PROP
        _prop = {
            'anyOf': [
                {
                    'type': 'object',
                    'title': cls._get_title(getattr(field, 'name', '')),
                    'properties': {
                        'type': {
                            'type': 'string',
                            'enum': ['Point']
                        },
                        'coordinates': _coord_prop
                    }
                },
                {**_coord_prop, 'title': cls._get_title(getattr(field, 'name', ''))}
            ]
        }

        if isinstance(field, (me.fields.LineStringField, me.fields.MultiPointField)):
            _prop['anyOf'][0]['properties']['type']['enum'] = ['LineString'] \
                if isinstance(field, me.fields.LineStringField) else ['MultiPoint']
            _coord_prop = {
                'type': 'array',
                'items': POINT_PROP
            }

        elif isinstance(field, (me.fields.PolygonField, me.fields.MultiLineStringField)):
            _prop['anyOf'][0]['properties']['type']['enum'] = ['Polygon'] \
                if isinstance(field, me.fields.PolygonField) else ['MultiLineString']
            _coord_prop = {
                'type': 'array',
                'items': {
                    'type': 'array',
                    'items': POINT_PROP
                }
            }

        elif isinstance(field, me.fields.MultiPolygonField):
            _prop['anyOf'][0]['properties']['type']['enum'] = ['MultiPolygon']
            _coord_prop = {
                'type': 'array',
                'items': {
                    'type': 'array',
                    'items': {
                        'type': 'array',
                        'items': POINT_PROP
                    }
                }
            }

        _prop['anyOf'][0]['properties']['coordinates'] = _coord_prop
        _prop['anyOf'][1] = {**_coord_prop, 'title': cls._get_title(getattr(field, 'name', ''))}
        return _prop

    @classmethod
    def _parse_list_field(cls, field: me.fields.ListField) -> dict:
        """
        Generates JSON schema for given list field and returns it.

        Args:
            field(me.fields.ListField): An instance of a MongoEngine ListField.

        Returns:
            dict
        """

        _field = getattr(field, 'field', None)
        field_dict = {'type': 'array'}

        if getattr(field, 'required', False):
            field_dict['minItems'] = 1

        if isinstance(_field, (me.fields.EmbeddedDocumentField, me.fields.GenericEmbeddedDocumentField)):
            field_dict['items'] = cls._parse_embedded_doc_field(_field)

        elif isinstance(_field, me.base.GeoJsonBaseField):
            field_dict['items'] = cls._parse_geo_field(_field)

        elif isinstance(_field, me.base.BaseField):
            field_dict['items'] = {'type': TYPE_MAP.get(type(_field).__name__, 'string')}

        return field_dict

    @classmethod
    def _parse(cls) -> dict:
        """
        Parses the MongoEngine document model and its fields. Generates and returns JSON schema for document. Fields
        are split into four categories: embedded document fields, list fields, geo JSON fields and base fields.

        Returns:
            dict
        """

        model_dict = {}
        for key, value in cls.__dict__.items():
            if not (isinstance(key, str) and
                    not key.startswith('_') and
                    key not in ['objects', 'id',
                                'DoesNotExist',
                                'MultipleObjectsReturned'] and
                    value is not None and not getattr(value, 'exclude_from_schema', False)):
                continue

            if isinstance(value, (me.fields.EmbeddedDocumentField, me.fields.GenericEmbeddedDocumentField)):
                model_dict = {**model_dict, key: cls._add_title(key, cls._parse_embedded_doc_field(value))}

            elif isinstance(value, me.fields.ListField):
                model_dict = {**model_dict, key: cls._add_title(key, cls._parse_list_field(value))}

            elif isinstance(value, me.base.GeoJsonBaseField):
                model_dict = {**model_dict, key: cls._parse_geo_field(value)}

            elif isinstance(value, me.base.BaseField):
                model_dict = {**model_dict, key: cls._add_title(key, cls._parse_field(value))}

        return model_dict

    @classmethod
    def json_schema(cls, strict: bool = True) -> dict:
        """
        Generates JSON schema.

        Args:
            strict(bool): If True, adds "required" key to schema. Defaults to True. Setting to False is useful for
                          validating JSONs when updating documents using HTTP PATCH method.

        Returns:
            dict
        """

        cls._STRICT = strict

        try:
            schema = getattr(cls, '_JSONSCHEMA')
            if not cls._STRICT and 'required' in schema.keys():
                del schema['required']
            return schema
        except AttributeError:
            pass

        model_properties = cls._parse()
        required_list = []
        for k, v in model_properties.items():
            req = v.get('required', False)
            if type(req) is bool:
                if req:
                    required_list.append(k)
                try:
                    del model_properties[k]['required']
                except KeyError:
                    continue

        schema = {
            '$id': f'/schemas/{cls.__name__}',
            'type': 'object',
            'title': f'{cls._get_title(cls.__name__)}',
            'properties': model_properties,
            'additionalProperties': True if issubclass(cls, (me.document.DynamicDocument,
                                                             me.document.DynamicEmbeddedDocument)) else False
        }

        if JsonSchemaMixin in cls.__bases__[0].__bases__:
            schema['properties'] = {**schema['properties'],
                                    **cls.__bases__[0].json_schema(strict=cls._STRICT)['properties']}

        if required_list and strict:
            schema['required'] = required_list

        return schema
