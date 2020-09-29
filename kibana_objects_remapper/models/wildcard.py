""" Wildcard handling implementation """

from bases import NestedObject
from actions import replace_keys, get_invalid_fields


class Wildcard(NestedObject):
    def convert(self):
        replace_keys(self.data)
        return self

    def validate(self):
        self.invalid_fields += get_invalid_fields(self.data.keys())
        return self
