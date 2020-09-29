""" Filters handling implementation """

from bases import NestedObject
import models
from actions import replace_value, get_invalid_fields


class AggParams(NestedObject):
    def convert(self):
        if self.has_filters:
            models.Filters(self.data['filters']).convert()
        if self.has_field:
            replace_value('field', self.data)

    def validate(self):
        if self.has_filters:
            self.invalid_fields += models.Filters(self.data['filters']).validate().get_invalid_fields()
        if self.has_field:
            self.invalid_fields += get_invalid_fields(self.data['field'])
        return self
