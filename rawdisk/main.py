# -*- coding: utf-8 -*-
import argparse
import logging
from rawdisk.util.logging import setup_logging
from rawdisk.session import Session
from rawdisk import scheme

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--verbose', help='increase output verbosity', action='store_true')

    parser.add_argument(
        '-f', '--file', dest='filename', help='specify source file',
        required=True
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

    if args is None or args.filename is None:
        logger.error('-f FILENAME must be specified')
        exit(0)

    session = Session()
    session.load_plugins()

    try:
        session.load(args.filename)
    except IOError:
        logger.error(
            'Failed to open disk image file: {}'.format(args.filename))
        exit(1)

    if session.partition_scheme == scheme.common.SCHEME_MBR:
        print('Scheme: MBR')
    elif session.partition_scheme == scheme.common.SCHEME_GPT:
        print('Scheme: GPT')
    else:
        print('Scheme: Unknown')

    print('Partitions:')
    session.volumes()

if __name__ == '__main__':
    main()
