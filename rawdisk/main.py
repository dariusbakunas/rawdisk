# -*- coding: utf-8 -*-
import argparse
import logging
import sys
from collections import namedtuple

from rawdisk.util.logging import setup_logging
from rawdisk.session import Session
from rawdisk.scheme.common import PartitionScheme

def parse_args(args):
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

    parsed_args = parser.parse_args(args)

    Options = namedtuple('Options', ['log_level', 'log_config', 'filename'])

    options = Options(
        log_level='DEBUG' if parsed_args.verbose
            else parsed_args.log_level,
        log_config=parsed_args.log_config,
        filename=parsed_args.filename
    )

    return options

def configure_logging(args):
    logging_options = {}

    if args.log_config:
        logging_options['config_path'] = args.log_config

    if args.log_level:
        logging_options['log_level'] = logging.getLevelName(args.log_level)

    setup_logging(**logging_options)

def main():
    args = parse_args(sys.argv[1:])
    configure_logging(args)

    logger = logging.getLogger(__name__)

    session = Session()
    session.load_plugins()

    try:
        session.load(args.filename)
    except IOError:
        logger.error(
            'Failed to open disk image file: {}'.format(args.filename))
        exit(1)

    if session.partition_scheme == PartitionScheme.SCHEME_MBR:
        print('Scheme: MBR')
    elif session.partition_scheme == PartitionScheme.SCHEME_GPT:
        print('Scheme: GPT')
    else:
        print('Scheme: Unknown')

    print('Partitions:')
    for volume in session.volumes:
        print(volume)

if __name__ == '__main__':
    main()
