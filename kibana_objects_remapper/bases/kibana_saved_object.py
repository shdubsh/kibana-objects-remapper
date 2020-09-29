""" KibanaSavedObject interface """

from abc import ABCMeta, abstractmethod


class KibanaSavedObject:
    __metaclass__ = ABCMeta

    def __init__(self, data: dict):
        self.data = data
        self.type = self._get_type()
        self.source = self._get_source()
        self.title = self.source['title']
        self.metadata = self.source['kibanaSavedObjectMeta']['searchSourceJSON']
        self.invalid_fields = []

    def _get_type(self):
        if self.data.get('_type') is None:
            return self.data['type']
        else:
            return self.data['_type']

    def _get_source(self):
        if self.data.get('_source') is None:
            return self.data['attributes']
        else:
            return self.data['_source']

    @abstractmethod
    def convert(self):
        """ Translates field mappings in-place based on Config.field_mapping """
        raise NotImplementedError

    @abstractmethod
    def validate(self):
        """ Searches objects for fields not in Config.valid_fields """
        raise NotImplementedError

    def get_invalid_fields(self):
        """ Returns set of discovered invalid fields """
        return sorted(set(self.invalid_fields))

    @staticmethod
    def has_aggs(o):
        return o.get('aggs') is not None

    @staticmethod
    def has_filters(o):
        return o.get('filters') is not None

    @staticmethod
    def has_field(o):
        return o.get('field') is not None

    @staticmethod
    def has_params(o):
        return o.get('params') is not None

    @staticmethod
    def has_meta(o):
        return o.get('meta') is not None

    @staticmethod
    def has_columns(o):
        return o.get('columns') is not None

    @staticmethod
    def has_exists(o):
        return o.get('exists') is not None

    @staticmethod
    def has_wildcard(o):
        return o.get('wildcard') is not None

    @staticmethod
    def has_bool(o):
        return o.get('bool') is not None

    @staticmethod
    def has_query(o):
        return o.get('query') is not None

    @staticmethod
    def has_index(o):
        return o.get('index') is not None

    @staticmethod
    def has_embeddable_config(o):
        return o.get('embeddableConfig') is not None

    @staticmethod
    def has_references(o):
        return o.get('references') is not None

    def get_dict(self):
        return self.data
