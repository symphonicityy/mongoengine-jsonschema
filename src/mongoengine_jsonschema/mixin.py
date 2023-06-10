import typing
import re

import mongoengine as me
import mongoengine.base


TYPE_MAP = {
    'BinaryField': 'string',
    'BooleanField': 'boolean',
    'CachedReferenceField': 'string',
    'ComplexDateTimeField': 'string',
    'DateTimeField': 'string',
    'DecimalField': 'number',
    'DictField': 'object',
    'DynamicField': 'string',
    'EmailField': 'string',
    'EmbeddedDocumentField': 'object',
    'EmbeddedDocumentListField': 'array',
    'EnumField': 'string',
    'FileField': 'string',
    'FloatField': 'number',
    'GenericEmbeddedDocumentField': 'object',
    'GenericReferenceField': 'string',
    'GenericLazyReferenceField': 'string',
    'GeoPointField': 'array',
    'ImageField': 'string',
    'IntField': 'integer',
    'ListField': 'array',
    'LongField': 'integer',
    'MapField': 'object',
    'ObjectIdField': 'string',
    'ReferenceField': 'string',
    'LazyReferenceField': 'string',
    'SequenceField': 'string',
    'SortedListField': 'array',
    'StringField': 'string',
    'URLField': 'string',
    'UUIDField': 'string',
    'PointField': 'object',
    'LineStringField': 'object',
    'PolygonField': 'object',
    'MultiPointField': 'object',
    'MultiLineStringField': 'object',
    'MultiPolygonField': 'object'
}

ATTR_MAP = {'required': 'required',
            'default': 'default',
            'min_value': 'minimum',
            'max_value': 'maximum',
            'min_length': 'minLength',
            'max_length': 'maxLength',
            'choices': 'enum',
            'regex': 'pattern'}


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

        return prop | {'title': cls._get_title(name)}

    @classmethod
    def _parse_field(cls, field: me.fields.BaseField) -> dict:
        """
        Generates property JSON by parsing MongoEngine field's arguments and returns it.
        
        Args:
            field(me.fields.BaseField): An instance of any MongoEngine base field.

        Returns:
            dict
        """

        field_dict = {'type': TYPE_MAP[type(field).__name__]}
        for k, v in ATTR_MAP.items():
            try:
                _val = getattr(field, k)
            except AttributeError:
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
    def _parse_embedded_doc_field(cls, doc: me.fields.EmbeddedDocumentField):
        """
        Generates JSON schema for given EmbeddedDocumentField and returns it. Make sure the embedded document
        class also inherits this mixin class (JsonSchemaMixin) or this method will return an empty dictionary.

        Args:
            doc(me.fields.EmbeddedDocumentField): A MongoEngine EmbeddedDocumentField instance

        Returns:
            dict
        """

        try:
            return doc.document_type_obj.json_schema(strict=cls._STRICT)
        except AttributeError:
            return {}

    @classmethod
    def _parse_reference_field(cls, doc: me.fields.ReferenceField) -> dict:
        """
        Returns JSON schema reference of given ReferenceField instance with '$ref'.

        Args:
            doc(me.document.Document): A MongoEngine ReferenceField instance

        Returns:
            dict
        """

        return {'$ref': f'/schemas/{doc.document_type_obj.__name__}'}

    @classmethod
    def _parse_list_field(cls, field: me.fields.BaseField) -> dict:
        """
        Generates JSON schema for given list field and returns it.

        Args:
            field(me.fields.BaseField): An instance of a MongoEngine ListField.

        Returns:
            dict
        """

        field_dict = {'type': TYPE_MAP[type(field).__name__]}
        if isinstance(getattr(field, 'field'), me.fields.EmbeddedDocumentField):
            field_dict = {'type': 'array'} | {'items': cls._parse_embedded_doc_field(getattr(field, 'field'))}
        elif isinstance(getattr(field, 'field'), me.fields.ReferenceField):
            field_dict = {'type': 'array'} | {'items': cls._parse_reference_field(getattr(field, 'field'))}
        elif isinstance(getattr(field, 'field'), me.base.BaseField):
            field_dict['items'] = {'type': TYPE_MAP[type(getattr(field, 'field')).__name__]}

        return field_dict

    @classmethod
    def _parse(cls) -> dict:
        """
        Parses the MongoEngine document model and its fields. Generates and returns JSON schema for document.

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
            if isinstance(value, me.fields.EmbeddedDocumentField):
                model_dict = model_dict | {key: cls._add_title(key, cls._parse_embedded_doc_field(value))}
            elif isinstance(value, me.fields.ListField):
                model_dict = model_dict | {key: cls._add_title(key, cls._parse_list_field(value))}
            elif isinstance(value, me.fields.ReferenceField):
                model_dict = model_dict | {key: cls._add_title(key, cls._parse_reference_field(value))}
            elif isinstance(value, me.base.BaseField):
                model_dict = model_dict | {key: cls._add_title(key, cls._parse_field(value))}

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
            'additionalProperties': True if issubclass(cls, me.document.DynamicDocument) or
                                            issubclass(cls, me.document.DynamicEmbeddedDocument) else False
        }

        if JsonSchemaMixin in cls.__bases__ and JsonSchemaMixin in cls.__bases__[0].__bases__:
            schema['properties'] = schema['properties'] | cls.__bases__[0].json_schema(strict=cls._STRICT)['properties']

        if required_list and strict:
            schema['required'] = required_list

        return schema
