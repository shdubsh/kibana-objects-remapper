""" QueryString handling implementation """

from bases import NestedObject
from config import Config
from actions import get_invalid_fields

from luqum.parser import parser as lucene_parser
from luqum.utils import LuceneTreeTransformer


class QueryString(NestedObject):
    def convert(self):
        if self.has_query:
            if self.data['query'] in ['*', '']:
                self.data['query'] = ''  # ES7 doesn't like asterisk here even in lucene
                return self
            transformer = QueryStringTransformer()
            parsed = lucene_parser.parse(self.data['query'])
            for ecs_field, old_fields in Config.field_mapping.items():
                transformer.old_fields = old_fields
                transformer.ecs_field = ecs_field
                parsed = transformer.visit(parsed)
            self.data['query'] = str(parsed)
        return self

    def validate(self):
        if self.has_query:
            if self.data['query'] in ['*', '']:
                return self
            validator = QueryStringValidator()
            validator.valid_ecs_fields = Config.valid_fields
            parsed = lucene_parser.parse(self.data['query'])
            validator.visit(parsed)
            self.invalid_fields += validator.invalid_fields
        return self


class QueryStringTransformer(LuceneTreeTransformer):
    old_fields = []
    ecs_field = ''

    def visit_search_field(self, node, parents):
        prefix = ''
        if node.name[0] == '!':
            node.name = node.name[1:]
            prefix = '!'
        for key in self.old_fields:
            if any([
                node.name == key,
                node.name == key + '.raw',
                node.name == key + '.keyword'
            ]):
                node.name = prefix + self.ecs_field
        return node


class QueryStringValidator(LuceneTreeTransformer):
    valid_ecs_fields = []

    def __init__(self):
        self.invalid_fields = []

    def visit_search_field(self, node, parents):
        if node.name[0] == '!':
            node.name = node.name[1:]
        if node.name == '_exists_':
            return node
        self.invalid_fields += get_invalid_fields(node.name)
        return node