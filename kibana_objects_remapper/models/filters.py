""" Filters handling implementation """

from bases import NestedObject
import models


class Filters(NestedObject):
    def convert(self):
        for filt in self.data:
            if filt.get('input') is not None:
                if filt['input'].get('query') is not None:
                    if isinstance(filt['input']['query'], str):
                        models.QueryString(filt['input']).convert()
                    else:
                        models.Query(filt['input']).convert()
            if filt.get('bool') is not None:
                models.BoolQuery(filt['bool']).convert()
        return self

    def validate(self):
        for filt in self.data:
            if filt.get('input') is not None:
                if filt['input'].get('query') is not None:
                    if isinstance(filt['input']['query'], str):
                        self.invalid_fields += models.QueryString(filt['input'])\
                            .validate().get_invalid_fields()
                    else:
                        self.invalid_fields += models.Query(filt['input'])\
                            .validate().get_invalid_fields()
            if filt.get('bool') is not None:
                self.invalid_fields += models.BoolQuery(filt['bool'])\
                    .validate().get_invalid_fields()
        return self
