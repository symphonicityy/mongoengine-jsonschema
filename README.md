Limitations:
- filefield, imagefield fields not supported
- schemes arg for URLField
- domain_whitelist, allow_utf8_user, allow_ip_domain args for EmailField

Notes:
'BinaryField': 'string',  # handled as string
'CachedReferenceField': 'string',  # handled as string
'GenericReferenceField': 'string',  # handled as string
'GenericLazyReferenceField': 'string',  # handled as string
'ObjectIdField': 'string',  # handled as string
'ReferenceField': 'string',  # handled as string
'LazyReferenceField': 'string',  # handled as string
'SequenceField': 'integer',  # handled as integer
'UUIDField': 'string',  # handled as string