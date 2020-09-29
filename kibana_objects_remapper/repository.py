import json
from models.dashboard import KibanaDashboard
from models.visualization import KibanaVisualization
from models.search import KibanaSearch


class KibanaSavedObjectsRepository:
    def __init__(self, backup_file='export.json'):
        self.kibana_version = None
        self.raw_data = self._read_json(backup_file)
        self.data = [x for x in self.raw_data if x.get(self._get_type_selector()) in ['dashboard', 'visualization', 'search']]
        self._convert_metadata()

    def _read_json(self, backup_file='export.json'):
        if backup_file.split('.')[-1] == 'json':
            self.kibana_version = '5'
            with open(backup_file, 'r') as f:
                return json.loads(f.read())
        if backup_file.split('.')[-1] == 'ndjson':
            self.kibana_version = '7'
            with open(backup_file, 'r') as f:
                return [json.loads(x) for x in f.readlines()]

    def _convert_metadata(self) -> None:
        """ Certain keys in the Kibana saved object are serialized JSON.
        Converts these keys from dict -> str or str -> dict in place. """

        for o in self.data:
            object_base = self._get_base_object(o)
            object_base['kibanaSavedObjectMeta']['searchSourceJSON'] = \
                self._convert_json_format(
                    object_base['kibanaSavedObjectMeta']['searchSourceJSON'])
            if o[self._get_type_selector()] == 'visualization':
                object_base['visState'] = \
                    self._convert_json_format(object_base['visState'])
                object_base['uiStateJSON'] = \
                    self._convert_json_format(object_base['uiStateJSON'])
            if o[self._get_type_selector()] == 'dashboard':
                object_base['panelsJSON'] = \
                    self._convert_json_format(object_base['panelsJSON'])
                object_base['optionsJSON'] = \
                    self._convert_json_format(object_base['optionsJSON'])

    def _get_base_object(self, o):
        if self.kibana_version == '7':
            return o['attributes']
        if self.kibana_version == '5':
            return o['_source']
        raise RuntimeError('The export may be from an unsupported version of Kibana.')

    def _convert_json_format(self, metadata: (dict, str)) -> (dict, str):
        """ Convert between dict and str based on parameter type """
        if isinstance(metadata, str):
            return json.loads(metadata)
        else:
            return json.dumps(metadata)

    def _get_type_selector(self):
        return '_type' if self.kibana_version == '5' else 'type'

    def save(self, output_file: str, data: list = None) -> None:
        if data is not None:
            self.data = data
        self._convert_metadata()
        if self.kibana_version == '5':
            with open(output_file, 'w') as f:
                f.write(json.dumps(self.data))
        if self.kibana_version == '7':
            with open(output_file, 'w') as f:
                for o in self.data:
                    f.write(json.dumps(o) + '\n')

    def get_searches(self) -> list:
        """ Get list of KibanaSearch objects """
        return [KibanaSearch(x) for x in self.data if x[self._get_type_selector()] == 'search']

    def get_visualizations(self) -> list:
        """ Get list of KibanaVisualization objects """
        return [KibanaVisualization(x) for x in self.data if x[self._get_type_selector()] == 'visualization']

    def get_dashboards(self) -> list:
        """ Get list of KibanaDashboard objects """
        return [KibanaDashboard(x) for x in self.data if x[self._get_type_selector()] == 'dashboard']

    def get_all(self) -> list:
        """ Get list of all Kibana objects in repository """
        return self.get_searches() + self.get_visualizations() + self.get_dashboards()
