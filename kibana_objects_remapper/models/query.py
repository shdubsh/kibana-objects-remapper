""" Query handling implementation """

from bases import NestedObject
import models
from actions import replace_keys, get_invalid_fields


class Query(NestedObject):
    
    def convert(self):
        if self.is_match_all:
            return self  # match_all queries have no parameters
        if self.is_term:
            replace_keys(self.data['term'])
        if self.is_terms:
            replace_keys(self.data['terms'])
        if self.is_terms_set:
            replace_keys(self.data['terms_set'])
        if self.is_fuzzy:
            replace_keys(self.data['fuzzy'])
        if self.is_prefix:
            replace_keys(self.data['prefix'])
        if self.is_range:
            replace_keys(self.data['range'])
        if self.is_regexp:
            replace_keys(self.data['regexp'])
        if self.is_wildcard:
            replace_keys(self.data['wildcard'])
        if self.is_match:
            replace_keys(self.data['match'])
        if self.is_match_phrase:
            replace_keys(self.data['match_phrase'])
        if self.is_bool:
            models.BoolQuery(self.data['bool']).convert()
        if self.is_query_string:
            models.QueryString(self.data['query_string']).convert()
        if self.has_query:
            Query(self.data['query']).convert()
        return self

    def validate(self):
        if self.is_match_all:
            return self  # match_all queries have no parameters
        if self.is_term:
            self.invalid_fields += get_invalid_fields(self.data['term'].keys())
        if self.is_terms:
            self.invalid_fields += get_invalid_fields(self.data['terms'].keys())
        if self.is_terms_set:
            self.invalid_fields += get_invalid_fields(self.data['terms_set'].keys())
        if self.is_fuzzy:
            self.invalid_fields += get_invalid_fields(self.data['fuzzy'].keys())
        if self.is_prefix:
            self.invalid_fields += get_invalid_fields(self.data['prefix'].keys())
        if self.is_range:
            self.invalid_fields += get_invalid_fields(self.data['range'].keys())
        if self.is_regexp:
            self.invalid_fields += get_invalid_fields(self.data['regexp'].keys())
        if self.is_wildcard:
            self.invalid_fields += get_invalid_fields(self.data['wildcard'].keys())
        if self.is_match:
            self.invalid_fields += get_invalid_fields(self.data['match'].keys())
        if self.is_match_phrase:
            self.invalid_fields += get_invalid_fields(self.data['match_phrase'].keys())
        if self.is_bool:
            self.invalid_fields += models.BoolQuery(self.data['bool'])\
                .validate().get_invalid_fields()
        if self.is_query_string:
            self.invalid_fields += models.QueryString(self.data['query_string'])\
                .validate().get_invalid_fields()
        if self.has_query:
            self.invalid_fields += Query(self.data['query']).validate().get_invalid_fields()
        return self
