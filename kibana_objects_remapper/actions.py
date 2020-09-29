"""
Common actions.
"""

from config import Config


def replace_value(key: str, o: dict) -> None:
    """ Replaces value at key definition in dict with ECS-compliant field """
    for ecs_field, old_fields in Config.field_mapping.items():
        for old_field in old_fields:
            for of in [old_field, old_field + '.raw', old_field + '.keyword']:
                if o[key] == of:
                    o[key] = ecs_field


def replace_values(o: list) -> None:
    """ Replaces all values in list with ECS-compliant fields """
    for ecs_field, old_fields in Config.field_mapping.items():
        for old_field in old_fields:
            for i, field in enumerate(o):
                for of in [old_field, old_field + '.raw', old_field + '.keyword']:
                    if o[i] == of:
                        o[i] = ecs_field


def replace_keys(o: dict) -> None:
    """ Replaces all dict keys with ECS-compliant fields """
    for ecs_field, old_fields in Config.field_mapping.items():
        for old_field in old_fields:
            for of in [old_field, old_field + '.raw', old_field + '.keyword']:
                if o.get(of) is not None:
                    o[ecs_field] = o[of]
                    del o[of]


def is_compliant(value: str) -> bool:
    """ Checks value against list of valid ECS fields """
    for field in Config.valid_fields:
        if field[-1] == '*':
            output = '.'.join(value.split('.')[:-1]) == '.'.join(field.split('.')[:-1])
        else:
            output = field == value
        if output:
            return output
    return value in Config.ignore_fields


def get_invalid_fields(o: (list, str)) -> list:
    """ Takes a list or str and returns list of fields that are not ECS-compliant """
    invalid_fields = []
    if isinstance(o, list):
        for field in o:
            invalid_fields += get_invalid_fields(field)
    if isinstance(o, str):
        if not is_compliant(o):
            invalid_fields.append(o)
    return invalid_fields
