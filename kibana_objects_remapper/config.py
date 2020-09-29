import yaml
from ecs import ValidECSFieldsGenerator


class Config:
    old_index_pattern = None
    new_index_pattern = None
    wildcard_fields = None
    ignore_fields = None
    field_mapping = None
    valid_fields = None

    @staticmethod
    def parse_config(config_file):
        """ Takes path to YAML config file and populates Config static object with values """
        with open(config_file, 'r') as f:
            parsed = yaml.safe_load(f.read())
        Config.old_index_pattern = parsed['old_index_pattern']
        Config.new_index_pattern = parsed['new_index_pattern']
        Config.wildcard_fields = parsed['wildcard_fields']
        Config.ignore_fields = parsed['ignore_fields']
        Config.field_mapping = parsed['field_mapping']
        Config.valid_ecs_fields = parsed.get('valid_fields')

    @staticmethod
    def generate_valid_fields(ecs_template_file):
        if Config.valid_fields is None:
            Config.valid_fields = ValidECSFieldsGenerator().get_valid_fields(
                ecs_template_file, Config.wildcard_fields)
