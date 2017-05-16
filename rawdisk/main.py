# -*- coding: utf-8 -*-

import argparse
import os
import sys
import logging.config
import yaml
from .modes.cli.cli_mode import CliMode
from .modes.legacy.legacy_mode import LegacyMode


MODE_CLI = 'cli'
MODE_LEGACY = 'legacy'
MODES = [MODE_CLI, MODE_LEGACY]


def setup_logging(config_path=None, log_level=logging.INFO):
    """Setup logging configuration
    """

    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format':
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': log_level,
                'propagate': True
            },
            'yapsy': {
                'handlers': ['console'],
                'level': logging.INFO
            }
        }
    }

    if config_path:
        if os.path.exists(config_path):
            with open(config_path, 'rt') as f:
                config = yaml.safe_load(f.read())
        else:
            print('Specified path does not exist: {}, '
                  'using default config'.format(config_path))

    logging.config.dictConfig(config)


def parse_args():
    parser = argparse.ArgumentParser(
        usage='%s -m [{}]'.format(', '.join(MODES)) %
              os.path.basename(sys.argv[0])
    )

    parser.add_argument(
        '-m', '--mode', help='select mode', choices=MODES, required=True)

    parser.add_argument(
        '--verbose', help='increase output verbosity', action='store_true')

    parser.add_argument(
        '-f', '--file', dest='filename', help='specify source file',
    )

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
    global logger

    args = parse_args()

    logging_options = {}

    if args.log_config:
        logging_options['config_path'] = args.log_config

    if args.verbose:
        logging_options['log_level'] = logging.DEBUG
    elif args.log_level:
        logging_options['log_level'] = logging.getLevelName(args.log_level)

    setup_logging(**logging_options)
    logger = logging.getLogger(__name__)

    if args.mode == MODE_CLI:
        CliMode.entry(args)
    else:
        LegacyMode.entry(args)


if __name__ == '__main__':
    main()
