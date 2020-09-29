""" KibanaSavedObject implementation for Dashboards """

from bases import KibanaSavedObject
import models
from config import Config
from actions import replace_keys, replace_value, replace_values, get_invalid_fields


class KibanaDashboard(KibanaSavedObject):
    def convert(self):
        if self.has_index(self.metadata):
            self.metadata['index'] = Config.new_index_pattern
        if self.has_references(self.data):
            for ref in self.data['references']:
                if ref['id'] == Config.old_index_pattern:
                    ref['id'] = Config.new_index_pattern
        for item in self.metadata['filter']:
            if self.has_meta(item):
                models.Meta(item['meta']).convert()
            if self.has_exists(item):
                replace_value('field', item['exists'])
            if self.has_wildcard(item):
                replace_keys(item['wildcard'])
            if self.has_bool(item):
                models.BoolQuery(item['bool']).convert()
            if self.has_query(item):
                models.Query(item['query']).convert()
        if self.has_query(self.metadata):
            models.QueryString(self.metadata['query']).convert()
        if self.has_panelsjson:
            for item in self.source['panelsJSON']:
                if self.has_columns(item):
                    replace_values(item['columns'])
                if self.has_embeddable_config(item):
                    models.EmbeddableConfig(item['embeddableConfig']).convert()
        return self

    def validate(self):
        for item in self.metadata['filter']:
            if self.has_meta(item):
                self.invalid_fields += models.Meta(item['meta'])\
                    .validate().get_invalid_fields()
            if self.has_exists(item):
                self.invalid_fields += get_invalid_fields(item['exists']['field'])
            if self.has_wildcard(item):
                self.invalid_fields += get_invalid_fields(item['wildcard'].keys())
            if self.has_bool(item):
                self.invalid_fields += models.BoolQuery(item['bool'])\
                    .validate().get_invalid_fields()
            if self.has_query(item):
                self.invalid_fields += models.Query(item['query'])\
                    .validate().get_invalid_fields()
        if self.has_query(self.metadata):  # Kibana 7 'query' at this level is a QueryString
            self.invalid_fields += models.QueryString(self.metadata['query'])\
                .validate().get_invalid_fields()
        if self.has_panelsjson:
            for item in self.source['panelsJSON']:
                if self.has_columns(item):
                    self.invalid_fields += get_invalid_fields(item['columns'])
                if self.has_embeddable_config(item):
                    self.invalid_fields += models.EmbeddableConfig(item['embeddableConfig'])\
                        .validate().get_invalid_fields()
        return self

    @property
    def has_panelsjson(self):
        return self.source.get('panelsJSON') is not None
