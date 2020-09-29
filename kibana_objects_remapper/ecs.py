"""
Generates a list of fields supported by the provided Elasticsearch ECS template.
"""
import json
from types import GeneratorType
from typing import Iterable


class ValidECSFieldsGenerator:
    def _is_leaf(self, o: dict) -> bool:
        """ Takes the current node and determines if it is a leaf node. """
        return o.get('properties') is None

    def _construct_branch(self, o: dict) -> (list, None):
        """ Takes the current node and builds the rest of the branch. """
        if not self._is_leaf(o):
            return [(k, self._construct_branch(v)) for k, v in o['properties'].items()]

    def _get_branch(self, o: dict, branch: list = None) -> GeneratorType:
        """ Generates the branch of the tree in list form."""
        if branch is None:
            branch = []
        if self._is_leaf(o):
            yield branch
        else:
            for k, v in o['properties'].items():
                yield self._get_branch(v, branch + [k])

    def _join_and_flatten(self, lst: Iterable, output: list, separator: str = '.') -> None:
        """
        Joins each branch node with the provided separator and flattens it all into one list of
        seperator-joined strings.
        """
        for item in lst:
            if isinstance(item, GeneratorType):
                self._join_and_flatten(item, output)
            else:
                output.append(separator.join(item))

    def _append_custom_kv_pair_fields(self, lst: list, wildcard_fields: list = None) -> list:
        """ Adds a globbing wildcard to fields that support custom key/value pairs. """
        if wildcard_fields is None:
            return lst
        for item in wildcard_fields:
            lst[lst.index(item)] = item + '.*'
        return lst

    def get_valid_fields(self, ecs_template: str, wildcard_fields: list = None) -> list:
        """ Takes a path to an ECS template and returns a list of dot-delimited paths. """
        with open(ecs_template, 'r') as f:
            parsed = json.loads(f.read())
        output = []
        for k, v in parsed['mappings']['properties'].items():
            self._join_and_flatten(self._get_branch(v, [k]), output)
        return self._append_custom_kv_pair_fields(output, wildcard_fields)


if __name__ == '__main__':
    from pprint import PrettyPrinter
    from sys import argv
    wildcard_fields = [
        'http.request.headers',
        'http.response.headers',
        'labels'
    ]

    PrettyPrinter().pprint(ValidECSFieldsGenerator().get_valid_fields(argv[1], wildcard_fields))
