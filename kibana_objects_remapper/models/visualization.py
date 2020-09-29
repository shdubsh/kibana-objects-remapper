""" KibanaSavedObject implementation for Visualizations """

from bases import KibanaSavedObject
import models
from config import Config
from actions import replace_value, replace_keys, get_invalid_fields


class KibanaVisualization(KibanaSavedObject):
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
        if self.has_query(self.metadata):  # Kibana 7
            if self.has_query(self.metadata['query']):
                models.QueryString(self.metadata['query']).convert()
            else:
                models.Query(self.metadata['query']).convert()
        if self.has_visState:
            if self.has_aggs(self.source['visState']):
                for agg in self.source['visState']['aggs']:
                    models.Agg(agg).convert()
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
        if self.has_query(self.metadata):
            models.QueryString(self.metadata['query'])\
                .validate().get_invalid_fields()
        if self.has_visState:
            if self.has_aggs(self.source['visState']):
                for agg in self.source['visState']['aggs']:
                    self.invalid_fields += models.Agg(agg)\
                        .validate().get_invalid_fields()
        return self

    @property
    def has_visState(self):
        return self.source.get('visState') is not None
