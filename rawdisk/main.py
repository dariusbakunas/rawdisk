from optparse import OptionParser
import os
import sys
import rawdisk
from rawdisk.plugins.manager import Manager
import logging


def main():
    logging.basicConfig(level=logging.INFO)

    parser = OptionParser(
        usage='Usage: %s -f <source>' %
        os.path.basename(sys.argv[0])
    )

    parser.add_option(
        '-f', '--file', dest='filename', type='string',
        help='specify source file'
    )

    (options, args) = parser.parse_args()

    if options.filename is None:
        parser.error('Filename not given')

    Manager.load_filesystem_plugins()

    r = rawdisk.reader.Reader()
    r.load(options.filename)
    print "Partitions:"
    r.list_partitions()