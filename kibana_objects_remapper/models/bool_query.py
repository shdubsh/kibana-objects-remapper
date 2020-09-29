""" BoolQuery handling implementation """

from bases import NestedObject
import models


class BoolQuery(NestedObject):
    def convert(self):
        for x in self.data.values():
            if isinstance(x, list):
                for item in x:
                    models.Query(item).convert()
        return self

    def validate(self):
        for x in self.data.values():
            if isinstance(x, list):
                for item in x:
                    self.invalid_fields += models.Query(item).validate().get_invalid_fields()
        return self
