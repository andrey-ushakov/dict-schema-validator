# dict-schema-validator
Validate python dictionaries (mongodb docs etc) using a JSON schema.

# JSON Schema example
Here is a simple schema representing a `Customer`:
```json
{
  "_id":          "ObjectId",
  "created":      "date",
  "is_active":    "bool",
  "fullname":     "string",
  "age":          ["int", "null"],
  "contact": {
    "phone":      "string",
    "email":      "string"
  },
  "cards": [{
    "type":       "string",
    "expires":    "date"
  }]
}
```

# Getting Started
```python
from datetime import datetime
import json
from dict_schema_validator import validator


with open('models/customer.json', 'r') as j:
    schema = json.loads(j.read())

customer = {
    "_id":          123,
    "created":      datetime.now(),
    "is_active":    True,
    "fullname":     "Jorge York",
    "age":          32,
    "contact": {
        "phone":      "559-940-1435",
        "email":      "york@example.com",
        "skype":      "j.york123"
    },
    "cards": [
        {"type": "visa", "expires": "12/2029"},
        {"type": "visa"},
    ]
}

errors = validator.validate(schema, customer)
for err in errors:
    print(err['msg'])
```

Output:
```
[*] "_id" has wrong type. Expected: "ObjectId", found: "int"
[+] Extra field: "contact.skype" having type: "str"
[*] "cards[0].expires" has wrong type. Expected: "date", found: "str"
[-] Missing field: "cards[1].expires"
```

# Supported Field Types
- string
- bool
- int
- float
- number (value can have `int` or `float` type)
- date (for `datetime`)
- null (for `None` values)
- ObjectId (for `bson.objectid.ObjectId`)


# JSON Schema Format
- Exact type: "field_1" : "type"
- One of the possible types: "field_1" : ["type1", "type2"]
- Define a dictionary: "field_1": {"field_1_1" : "type", ...}
- Define an array: "field_1": [ {"field_1_1" : "type", ...} ]


# TODO
 - enums for string type
 - value validators
 - required (true, false) attribute for fields
 - array of base types support