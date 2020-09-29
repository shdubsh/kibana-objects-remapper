""" Agg handling implementation """

from bases import NestedObject
from models import AggParams


class Agg(NestedObject):
    def convert(self):
        if self.has_params:
            AggParams(self.data['params']).convert()

    def validate(self):
        if self.has_params:
            self.invalid_fields += AggParams(self.data['params']).validate().get_invalid_fields()
        return self
