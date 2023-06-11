### Example document and JSON schema output

```python 
from enum import Enum

import mongoengine as me
from mongoengine_jsonschema import JsonSchemaMixin


class ChoiceEnum(Enum):  # for EnumField
    A = '1'
    B = '2'
    C = '3'


class ExampleBaseDocument(me.Document, JsonSchemaMixin):
    meta = {'allow_inheritance': True}
    base_field = me.StringField()


class ExampleEmbeddedDocument(me.EmbeddedDocument, JsonSchemaMixin):
    embedded_field = me.StringField()


class ExampleReferencedDocument(me.Document, JsonSchemaMixin):
    pass


class ExampleDocument(me.Document):
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
    int_field = me.IntField(min_value=0, max_value=1)
    lazy_reference_field = me.LazyReferenceField(ExampleReferencedDocument)
    line_string_field = me.LineStringField()
    list_field = me.ListField(me.StringField(), required=True)
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
```

Calling `ExampleDocument.json_schema()` returns

```python
{
   "$id":"/schemas/ExampleDocument",
   "type":"object",
   "title":"Example Document",
   "properties":{
      "binary_field":{
         "type":"string",
         "title":"Binary Field"
      },
      "boolean_field":{
         "type":"boolean",
         "title":"Boolean Field"
      },
      "cached_reference_field":{
         "type":"string",
         "title":"Cached Reference Field"
      },
      "complex_datetime_field":{
         "type":"string",
         "format":"date-time",
         "title":"Complex Datetime Field"
      },
      "datetime_field":{
         "type":"string",
         "format":"date-time",
         "title":"Datetime Field"
      },
      "date_field":{
         "type":"string",
         "format":"date",
         "title":"Date Field"
      },
      "decimal_field":{
         "type":"number",
         "title":"Decimal Field"
      },
      "dict_field":{
         "type":"object",
         "default":{
            
         },
         "title":"Dict Field"
      },
      "dynamic_field":{
         "default":1,
         "title":"Dynamic Field"
      },
      "email_field":{
         "type":"string",
         "format":"email",
         "title":"Email Field"
      },
      "embedded_document_field":{
         "$id":"/schemas/ExampleEmbeddedDocument",
         "type":"object",
         "title":"Embedded Document Field",
         "properties":{
            "embedded_field":{
               "type":"string",
               "title":"Embedded Field"
            }
         },
         "additionalProperties":false
      },
      "embedded_document_list_field":{
         "type":"array",
         "items":{
            "$id":"/schemas/ExampleEmbeddedDocument",
            "type":"object",
            "title":"Example Embedded Document",
            "properties":{
               "embedded_field":{
                  "type":"string",
                  "title":"Embedded Field"
               }
            },
            "additionalProperties":false
         },
         "title":"Embedded Document List Field"
      },
      "enum_field":{
         "type":"string",
         "enum":[
            "1",
            "2",
            "3"
         ],
         "title":"Enum Field"
      },
      "float_field":{
         "type":"number",
         "title":"Float Field"
      },
      "generic_embedded_document_field":{
         "type":"object",
         "title":"Generic Embedded Document Field"
      },
      "generic_lazy_reference_field":{
         "type":"string",
         "enum":[
            
         ],
         "title":"Generic Lazy Reference Field"
      },
      "generic_reference_field":{
         "type":"string",
         "enum":[
            
         ],
         "title":"Generic Reference Field"
      },
      "geo_point_field":{
         "type":"array",
         "prefixItems":[
            {
               "type":"number",
               "min_value":-180,
               "max_value":180
            },
            {
               "type":"number",
               "min_value":-90,
               "max_value":90
            }
         ],
         "items":false,
         "title":"Geo Point Field"
      },
      "int_field":{
         "type":"integer",
         "minimum":0,
         "maximum":1,
         "title":"Int Field"
      },
      "lazy_reference_field":{
         "type":"string",
         "title":"Lazy Reference Field"
      },
      "line_string_field":{
         "anyOf":[
            {
               "type":"object",
               "title":"Line String Field",
               "properties":{
                  "type":{
                     "type":"string",
                     "enum":[
                        "LineString"
                     ]
                  },
                  "coordinates":{
                     "type":"array",
                     "items":{
                        "type":"array",
                        "prefixItems":[
                           {
                              "type":"number",
                              "min_value":-180,
                              "max_value":180
                           },
                           {
                              "type":"number",
                              "min_value":-90,
                              "max_value":90
                           }
                        ],
                        "items":false
                     }
                  }
               }
            },
            {
               "type":"array",
               "items":{
                  "type":"array",
                  "prefixItems":[
                     {
                        "type":"number",
                        "min_value":-180,
                        "max_value":180
                     },
                     {
                        "type":"number",
                        "min_value":-90,
                        "max_value":90
                     }
                  ],
                  "items":false
               },
               "title":"Line String Field"
            }
         ]
      },
      "list_field":{
         "type":"array",
         "minItems":1,
         "items":{
            "type":"string"
         },
         "title":"List Field"
      },
      "long_field":{
         "type":"integer",
         "title":"Long Field"
      },
      "map_field":{
         "type":"object",
         "patternProperties":{
            ".*":{
               "type":"integer"
            }
         },
         "default":{
            
         },
         "title":"Map Field"
      },
      "multi_line_string_field":{
         "anyOf":[
            {
               "type":"object",
               "title":"Multi Line String Field",
               "properties":{
                  "type":{
                     "type":"string",
                     "enum":[
                        "MultiLineString"
                     ]
                  },
                  "coordinates":{
                     "type":"array",
                     "items":{
                        "type":"array",
                        "items":{
                           "type":"array",
                           "prefixItems":[
                              {
                                 "type":"number",
                                 "min_value":-180,
                                 "max_value":180
                              },
                              {
                                 "type":"number",
                                 "min_value":-90,
                                 "max_value":90
                              }
                           ],
                           "items":false
                        }
                     }
                  }
               }
            },
            {
               "type":"array",
               "items":{
                  "type":"array",
                  "items":{
                     "type":"array",
                     "prefixItems":[
                        {
                           "type":"number",
                           "min_value":-180,
                           "max_value":180
                        },
                        {
                           "type":"number",
                           "min_value":-90,
                           "max_value":90
                        }
                     ],
                     "items":false
                  }
               },
               "title":"Multi Line String Field"
            }
         ]
      },
      "multi_point_field":{
         "anyOf":[
            {
               "type":"object",
               "title":"Multi Point Field",
               "properties":{
                  "type":{
                     "type":"string",
                     "enum":[
                        "MultiPoint"
                     ]
                  },
                  "coordinates":{
                     "type":"array",
                     "items":{
                        "type":"array",
                        "prefixItems":[
                           {
                              "type":"number",
                              "min_value":-180,
                              "max_value":180
                           },
                           {
                              "type":"number",
                              "min_value":-90,
                              "max_value":90
                           }
                        ],
                        "items":false
                     }
                  }
               }
            },
            {
               "type":"array",
               "items":{
                  "type":"array",
                  "prefixItems":[
                     {
                        "type":"number",
                        "min_value":-180,
                        "max_value":180
                     },
                     {
                        "type":"number",
                        "min_value":-90,
                        "max_value":90
                     }
                  ],
                  "items":false
               },
               "title":"Multi Point Field"
            }
         ]
      },
      "multi_polygon_field":{
         "anyOf":[
            {
               "type":"object",
               "title":"Multi Polygon Field",
               "properties":{
                  "type":{
                     "type":"string",
                     "enum":[
                        "MultiPolygon"
                     ]
                  },
                  "coordinates":{
                     "type":"array",
                     "items":{
                        "type":"array",
                        "items":{
                           "type":"array",
                           "items":{
                              "type":"array",
                              "prefixItems":[
                                 {
                                    "type":"number",
                                    "min_value":-180,
                                    "max_value":180
                                 },
                                 {
                                    "type":"number",
                                    "min_value":-90,
                                    "max_value":90
                                 }
                              ],
                              "items":false
                           }
                        }
                     }
                  }
               }
            },
            {
               "type":"array",
               "items":{
                  "type":"array",
                  "items":{
                     "type":"array",
                     "items":{
                        "type":"array",
                        "prefixItems":[
                           {
                              "type":"number",
                              "min_value":-180,
                              "max_value":180
                           },
                           {
                              "type":"number",
                              "min_value":-90,
                              "max_value":90
                           }
                        ],
                        "items":false
                     }
                  }
               },
               "title":"Multi Polygon Field"
            }
         ]
      },
      "object_ID_field":{
         "type":"string",
         "title":"Object ID Field"
      },
      "point_field":{
         "anyOf":[
            {
               "type":"object",
               "title":"Point Field",
               "properties":{
                  "type":{
                     "type":"string",
                     "enum":[
                        "Point"
                     ]
                  },
                  "coordinates":{
                     "type":"array",
                     "prefixItems":[
                        {
                           "type":"number",
                           "min_value":-180,
                           "max_value":180
                        },
                        {
                           "type":"number",
                           "min_value":-90,
                           "max_value":90
                        }
                     ],
                     "items":false
                  }
               }
            },
            {
               "type":"array",
               "prefixItems":[
                  {
                     "type":"number",
                     "min_value":-180,
                     "max_value":180
                  },
                  {
                     "type":"number",
                     "min_value":-90,
                     "max_value":90
                  }
               ],
               "items":false,
               "title":"Point Field"
            }
         ]
      },
      "polygon_field":{
         "anyOf":[
            {
               "type":"object",
               "title":"Polygon Field",
               "properties":{
                  "type":{
                     "type":"string",
                     "enum":[
                        "Polygon"
                     ]
                  },
                  "coordinates":{
                     "type":"array",
                     "items":{
                        "type":"array",
                        "items":{
                           "type":"array",
                           "prefixItems":[
                              {
                                 "type":"number",
                                 "min_value":-180,
                                 "max_value":180
                              },
                              {
                                 "type":"number",
                                 "min_value":-90,
                                 "max_value":90
                              }
                           ],
                           "items":false
                        }
                     }
                  }
               }
            },
            {
               "type":"array",
               "items":{
                  "type":"array",
                  "items":{
                     "type":"array",
                     "prefixItems":[
                        {
                           "type":"number",
                           "min_value":-180,
                           "max_value":180
                        },
                        {
                           "type":"number",
                           "min_value":-90,
                           "max_value":90
                        }
                     ],
                     "items":false
                  }
               },
               "title":"Polygon Field"
            }
         ]
      },
      "reference_field":{
         "type":"string",
         "title":"Reference Field"
      },
      "sequence_field":{
         "type":"integer",
         "title":"Sequence Field"
      },
      "sorted_list_field":{
         "type":"array",
         "items":{
            "type":"integer"
         },
         "title":"Sorted List Field"
      },
      "string_field":{
         "type":"string",
         "default":"1",
         "minLength":1,
         "maxLength":2,
         "enum":[
            "1",
            "2",
            "3"
         ],
         "pattern":".*",
         "title":"String Field"
      },
      "URL_field":{
         "type":"string",
         "format":"uri",
         "pattern":"^(?:[a-z0-9\\.\\-]*)://(?:(?:[A-Z0-9](?:[A-Z0-9-_]{0,61}[A-Z0-9])?\\.)+(?:[A-Z]{2,6}\\.?|[A-Z0-9-]{2,}(?<!-)\\.?)|localhost|\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}|\\[?[A-F0-9]*:[A-F0-9:]+\\]?)(?::\\d+)?(?:/?|[/?]\\S+)$",
         "title":"URL Field"
      },
      "UUID_field":{
         "type":"string",
         "format":"uuid",
         "title":"UUID Field"
      }
   },
   "additionalProperties":false,
   "required":[
      "boolean_field"
   ]
}
```