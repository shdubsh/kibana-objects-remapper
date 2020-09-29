""" EmbeddableConfig handling implementation """

from bases import NestedObject
from actions import replace_values, get_invalid_fields


class EmbeddableConfig(NestedObject):
    def convert(self):
        if self.has_columns:
            replace_values(self.data['columns'])
        return self

    def validate(self):
        if self.has_columns:
            self.invalid_fields += get_invalid_fields(self.data['columns'])
        return self
