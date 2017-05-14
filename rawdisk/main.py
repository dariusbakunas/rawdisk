# -*- coding: utf-8 -*-

import argparse
import os
import sys
import rawdisk
import logging.config
import yaml
from . import scheme


def setup_logging(config_path='logging.yaml', default_level=logging.INFO):
    """Setup logging configuration
    """
    path = config_path

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def main():
    parser = argparse.ArgumentParser(
        usage='Usage: %s -f <source>' %
        os.path.basename(sys.argv[0])
    )

    parser.add_argument(
        "--verbose", help="increase output verbosity", action="store_true")

    parser.add_argument(
        '-f', '--file', dest='filename', help='specify source file',
    )

    parser.add_argument(
        '--log-config', dest='log_config', help='path to logging configuration file'
    )

    parser.add_argument(
        '--log-level', dest='log_level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    )

    args = parser.parse_args()

    setup_logging()
    logger = logging.getLogger(__name__)

    if args.filename is None:
        parser.print_help()
    else:
        r = rawdisk.reader.Reader()

        try:
            r.load(args.filename)
        except IOError:
            logger.error('Failed to open disk image file: {}'.format(args.filename))

        if r.scheme == scheme.common.SCHEME_MBR:
            print("Scheme: MBR")
        elif r.scheme == scheme.common.SCHEME_GPT:
            print("Scheme: GPT")
        else:
            print("Scheme: Unknown")

        print("Partitions:")
        r.list_partitions()
