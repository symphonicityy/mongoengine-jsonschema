# JSON Schema Generator for MongoEngine Documents

## 📖 About the project

### What is this and why?
This package provides a mixin class that extends a MongoEngine document's functionality by adding a `.json_schema()` method and allows generating a JSON schema directly from the document. Generated schema then can be used in API documentation or form validation and automatic form generation on a web application frontend, etc.

Generated schema should be compatible with [JSON schema specification](https://json-schema.org/specification.html) version Draft-7 and newer.

Tested on
- Python 3.10
- MongoEngine 0.27.0

but should work on Python >= `3.7` and MongoEngine >= `0.20.0` without any problems.

## 🛠 Installation

```sh
pip install mongoengine-jsonschema
```

## 💻 Getting started
Add `JsonSchemaMixin` to your document class as parent. Resolution order matters, so always place MongoEngine document first.
```python
import mongoengine as me
from mongoengine_jsonschema import JsonSchemaMixin

class Person(me.Document, JsonSchemaMixin):
    name = me.StringField(required=True, min_length=1, max_length=32)
    age = me.IntField(min_value=0)

```
Then you can generate JSON schema by calling `.json_schema()` method.
```python
Person.json_schema()
```
which returns the schema as a Python dictionary
```python
{
    '$id': '/schemas/Person',
    'title': 'Person',
    'type': 'object',
    'properties': {
        'age': {
            'type': 'integer',
            'title': 'Age',
            'minimum': 0
        },
        'name': {
            'type': 'string',
            'title': 'Name',
            'minLength': 1,
            'maxLength': 32
        }
    },
    'required': ['name'],
    'additionalProperties': False
}
```

### Example
Check out [example.md](https://github.com/symphonicityy/mongoengine-jsonschema/blob/main/example.md) for a more extensive example.

### Features
- Inheritance is supported. Make sure you add mixin to parent class.
- `additionalProperties` is set to `False` for `DynamicDocument` and `DynamicEmbeddedDocument` classes.
- `required` keyword can be removed by setting `strict` argument to `False` (`.json_schema(strict=False)`). This is useful for partial validation when updating documents using HTTP PATCH method.
- Constraints for special `StringField` types such as `EmailField`, `URLField`, `UUIDField`, `DateTimeField` etc. are applied to schema using `format` and/or `pattern` keywords.
- Fields derived from `GeoJsonBaseField` can be validated for both array and object types as supported by MongoEngine.
- Field arguments/constraints `required`, `min_length`, `max_length`, `min_value`, `max_value`, `default`, `choices`, `regex` and `url_regex` (for `URLField`) are supported and reflected to schema.
- Excluding a field from schema is possible with setting field argument `exclude_from_schema` to `True`. Example: 
    ```python 
    name = me.StringField(exclude_from_schema=True)
    ```
- Auto-generates human-friendly (first-letter capitalized, separate words) `title` from both document (PascalCase) and field names (snake_case). Keeps uppercase acronyms as is, e.g. `page_URL` -> `Page URL`.
- For `ListField` types, `required=True` means it cannot be empty, therefore, schema defines this constraint with `minItems` keyword.
- Custom schemas can be defined directly in model class with `_JSONSCHEMA` class attribute. Setting a `_JSONSCHEMA` attribute will bypass JSON schema generation.

### Limitations
- `FileField`, `ImageField` fields are not supported
- `PolygonField` and `MultiPolygonField` must start and end at the same point, but this is not enforced by generated schema
- `schemes` argument is ignored for `URLField`
- `domain_whitelist`, `allow_utf8_user`, `allow_ip_domain` arguments are ignored for `EmailField`
- The following fields are defined in schema as strings and may require field specific conversion before assigning to a document's attribute:
    - `ObjectIdField`
    - `BinaryField`
    - `DateTimeField`
    - `ComplexDateTimeField`
    - `DateField`
    - `ReferenceField`
    - `LazyReferenceField`
    - `CachedReferenceField`
    - `GenericReferenceField`
    - `GenericLazyReferenceField`


## 👥 Contact <a name="contact"/>
- Email: [myusuferoglu@gmail.com](<mailto:myusuferoglu@gmail.com>)
- GitHub: [symphonicityy](https://github.com/symphonicityy)
- Project Link: (https://github.com/symphonicityy/mongoengine-jsonschema)

## 🤝 Contributing <a name="contributing"/>
Contributions, issues, and feature requests are welcome!
