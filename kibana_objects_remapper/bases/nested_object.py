""" NestedObject interface """

from abc import ABCMeta, abstractmethod


class NestedObject:
    __metaclass__ = ABCMeta

    def __init__(self, data: dict):
        self.data = data
        self.invalid_fields = []

    @abstractmethod
    def convert(self):
        """ Translates field mappings in-place based on Config.field_mapping """
        raise NotImplementedError

    @abstractmethod
    def validate(self):
        """ Searches objects for fields not in Config.valid_fields """
        raise NotImplementedError

    def get_invalid_fields(self) -> list:
        """ Returns list of discovered invalid fields """
        return self.invalid_fields

    @property
    def is_match(self):
        return self.data.get('match') is not None

    @property
    def is_match_phrase(self):
        return self.data.get('match_phrase') is not None

    @property
    def is_match_all(self):
        return self.data.get('match_all') is not None

    @property
    def is_bool(self):
        return self.data.get('bool') is not None

    @property
    def is_query_string(self):
        return self.data.get('query_string') is not None

    @property
    def is_term(self):
        return self.data.get('term') is not None

    @property
    def is_terms(self):
        return self.data.get('terms') is not None

    @property
    def is_terms_set(self):
        return self.data.get('terms_set') is not None

    @property
    def is_fuzzy(self):
        return self.data.get('fuzzy') is not None

    @property
    def is_prefix(self):
        return self.data.get('prefix') is not None

    @property
    def is_range(self):
        return self.data.get('range') is not None

    @property
    def is_regexp(self):
        return self.data.get('regexp') is not None

    @property
    def is_wildcard(self):
        return self.data.get('wildcard') is not None

    @property
    def has_query(self):
        return self.data.get('query') is not None

    @property
    def has_index(self):
        return self.data.get('index') is not None

    @property
    def has_params(self):
        return self.data.get('params') is not None

    @property
    def has_filters(self):
        return self.data.get('filters') is not None

    @property
    def has_field(self):
        return self.data.get('field') is not None

    @property
    def has_bool(self):
        return self.data.get('bool') is not None

    @property
    def has_columns(self):
        return self.data.get('columns') is not None

    def get_dict(self):
        return self.data
