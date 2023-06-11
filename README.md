Limitations:
- filefield, imagefield fields are not supported
- PolygonField MultiPoligonField must start and end at the same point but not enforced by schema
- schemes arg for URLField
- domain_whitelist, allow_utf8_user, allow_ip_domain args for EmailField

Notes:
'BinaryField': 'string',  # handled as string
'DateTimeField': 'string',  # handled as string
'ComplexDateTimeField': 'string',  # handled as string
'DateField': 'string',  # handled as string
'CachedReferenceField': 'string',  # handled as string
'GenericReferenceField': 'string',  # handled as string
'GenericLazyReferenceField': 'string',  # handled as string
'ObjectIdField': 'string',  # handled as string
'ReferenceField': 'string',  # handled as string
'LazyReferenceField': 'string',  # handled as string