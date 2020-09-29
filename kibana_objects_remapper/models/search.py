""" KibanaSavedObject implementation for Searches """

from bases import KibanaSavedObject
import models
from config import Config
from actions import replace_keys, replace_value, replace_values, get_invalid_fields


class KibanaSearch(KibanaSavedObject):
    def convert(self):
        if self.has_index(self.metadata):
            self.metadata['index'] = Config.new_index_pattern
        if self.has_references(self.data):
            for ref in self.data['references']:
                if ref['id'] == Config.old_index_pattern:
                    ref['id'] = Config.new_index_pattern
        for o in self.metadata['filter']:
            if self.has_meta(o):
                models.Meta(o['meta']).convert()
            if self.has_exists(o):
                replace_value('field', o['exists'])
            if self.has_wildcard(o):
                replace_keys(o['wildcard'])
            if self.has_bool(o):
                models.BoolQuery(o['bool']).convert()
            if self.has_query(o):
                models.Query(o['query']).convert()
        if self.has_query(self.metadata):
            models.Query(self.metadata['query']).convert()
        if self.has_columns:
            replace_values(self.source['columns'])
        return self

    def validate(self):
        for o in self.metadata['filter']:
            if self.has_meta(o):
                self.invalid_fields += models.Meta(o['meta']).validate().get_invalid_fields()
            if self.has_exists(o):
                self.invalid_fields += get_invalid_fields(o['exists']['field'])
            if self.has_wildcard(o):
                self.invalid_fields += get_invalid_fields(o['wildcard'].keys())
            if self.has_bool(o):
                self.invalid_fields += models.bool_query.BoolQuery(o['bool']).validate().get_invalid_fields()
            if self.has_query(o):
                self.invalid_fields += models.query.Query(o['query']).validate().get_invalid_fields()
        if self.has_query(self.metadata):
            self.invalid_fields += models.Query(self.metadata['query']).validate().get_invalid_fields()
        if self.has_columns:
            self.invalid_fields += get_invalid_fields(self.source['columns'])
        return self
