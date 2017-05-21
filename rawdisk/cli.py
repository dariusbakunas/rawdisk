import argparse
import logging
import sys
from collections import namedtuple
from rawdisk.ui.cli.cli_mode import CliMode
from rawdisk.util.logging import setup_logging

def parse_args(args):
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

    parsed_args = parser.parse_args(args)

    Options = namedtuple('Options', ['log_level', 'log_config'])

    options = Options(
        log_level='DEBUG' if parsed_args.verbose
        else parsed_args.log_level,
        log_config=parsed_args.log_config
    )

    return options

def configure_logging(args):
    logging_options = {}

    if args.log_config:
        logging_options['config_path'] = args.log_config

    if args.log_level:
        logging_options['log_level'] = logging.getLevelName(args.log_level)

    logging_options['formatter'] = 'ui'

    setup_logging(**logging_options)

def main():
    args = parse_args(sys.argv[1:])
    configure_logging(args)

    CliMode.start()

if __name__ == '__main__':
    main()
