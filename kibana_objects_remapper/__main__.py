""" CLI Entrypoint """

import argparse
from config import Config
from repository import KibanaSavedObjectsRepository


def main(args):
    Config.parse_config(args.config_file)
    Config.generate_valid_fields(args.ecs_template_file)
    repository = KibanaSavedObjectsRepository(backup_file=args.kibana_backup_file)
    validated = [x.convert().validate() for x in repository.get_all()]
    output = []
    for o in validated:
        invalid_fields = o.get_invalid_fields()
        if invalid_fields:
            output.append('{} object "{}" uses fields: {}'.format(o.type, o.title, invalid_fields))
    for x in sorted(output):
        print(x)
    repository.save(args.kibana_output_file, [x.get_dict() for x in validated])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--kibana-backup-file', action='store', help='kibana backup file input')
    parser.add_argument('-e', '--ecs-template-file', action='store', help='ecs template file')
    parser.add_argument('-o', '--kibana-output-file', action='store', help='kibana backup file output')
    parser.add_argument('-c', '--config_file', action='store', help='config file')
    args = parser.parse_args()
    main(args)
