import bson
from datetime import datetime


def build_path(path, key):
    return key if len(path) == 0 else path + '.' + key


def validate_array(m, doc, path):
    result = []
    for i in range(len(doc)):
        result += validate(m, doc[i], path + '[{}]'.format(i))
    return result


def validate_type(value, type_str):
    if type_str == 'string':
        return type(value) is str
    elif type_str == 'bool':
        return type(value) is bool
    elif type_str == 'int':
        return type(value) is int
    elif type_str == 'float':
        return type(value) is float
    elif type_str == 'date':
        return type(value) is datetime
    elif type_str == 'null':
        return value is None
    elif type_str == 'ObjectId':
        return type(value) is bson.objectid.ObjectId
    elif type_str == 'number':
        return type(value) in [int, float]
    elif type_str == 'object':
        # Do not validate the object's structure
        return type(value) is dict
    elif type_str == 'any':
        return True
    else:
        raise Exception('Model type is not valid')


def validate(m, doc, path=''):
    result = []

    # Verify that passed document is a dictionary
    if type(doc) is not dict:
        raise Exception('Document passed to "validate" function must be a dictionary')

    # Check for extra fields in mongo doc
    for field in doc:
        if field not in m.keys():
            fullpath = build_path(path, field)
            field_type = type(doc[field]).__name__
            result.append({
                'msg': '[+] Extra field: "{}" having type: "{}"'.format(fullpath, field_type),
                'type': 'extra_field',
                'path': fullpath,
                'field_type': field_type
            })
            # log()

    for key in m:
        if key not in doc:
            # log()
            fullpath = build_path(path, key)
            result.append({
                'msg': '[-] Missing field: "{}"'.format(fullpath),
                'type': 'missing_field',
                'path': fullpath,
            })
            continue

        # Model field is an array of objects
        if type(m[key]) is list and type(m[key][0]) is dict:
            result += validate_array(m[key][0], doc[key], build_path(path, key))
            continue

        # Model field is an object
        if type(m[key]) is dict:
            result += validate(m[key], doc[key], build_path(path, key))
            continue

        # Model field is an array of strings (means data value can have any of the presented types)
        if type(m[key]) is list and type(m[key][0]) is str:
            res = any(validate_type(doc[key], cur_type) for cur_type in m[key])
            if not res:
                # log()
                fullpath = build_path(path, key)
                expected = m[key]
                found = type(doc[key]).__name__
                result.append({
                    'msg': '[*] "{}" has wrong type. Expected one of: "{}", found: "{}"'.format(fullpath, expected,found),
                    'type': 'wrong_type',
                    'path': fullpath,
                    'expected': expected,
                    'found': found,
                })
            continue

        # Model field is a string
        res = None
        try:
            res = validate_type(doc[key], m[key])
        except Exception as e:
            raise Exception('[@@@] Model is not valid: "{}" has incorrect type: "{}"'.format(key, m[key]))
        if not res:
            # log()
            fullpath = build_path(path, key)
            expected = m[key]
            found = type(doc[key]).__name__
            result.append({
                'msg': '[*] "{}" has wrong type. Expected: "{}", found: "{}"'.format(fullpath, expected, found),
                'type': 'wrong_type',
                'path': fullpath,
                'expected': expected,
                'found': found,
            })
    return result
