""" Meta handling implementation """

from bases import NestedObject
from actions import replace_value, get_invalid_fields
from config import Config


class Meta(NestedObject):
    def convert(self):
        replace_value('key', self.data)
        if self.has_index:
            self.data['index'] = Config.new_index_pattern
        return self

    def validate(self):
        self.invalid_fields += get_invalid_fields(self.data['key'])
        return self
