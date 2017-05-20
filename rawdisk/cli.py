import argparse
import logging
from rawdisk.ui.cli.cli_mode import CliMode
from rawdisk.util.logging import setup_logging

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--verbose', help='increase output verbosity', action='store_true')

    parser.add_argument(
        '--log-config', dest='log_config',
        help='path to YAML logging configuration file'
    )

    parser.add_argument(
        '--log-level', dest='log_level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    )

    args = parser.parse_args()

    return args

def main():
    args = parse_args()

    logging_options = {}

    if args.log_config:
        logging_options['config_path'] = args.log_config

    if args.verbose:
        logging_options['log_level'] = logging.DEBUG
    elif args.log_level:
        logging_options['log_level'] = logging.getLevelName(args.log_level)

    setup_logging(**logging_options)

    CliMode.start()

if __name__ == '__main__':
    main()
