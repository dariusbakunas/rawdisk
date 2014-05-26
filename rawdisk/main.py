from optparse import OptionParser
import os
import sys
import rawdisk
import logging
import scheme


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

    r = rawdisk.reader.Reader()
    r.load(options.filename)

    if (r.scheme == scheme.common.SCHEME_MBR):
        print "Scheme: MBR"
    elif (r.scheme == scheme.common.SCHEME_GPT):
        print "Scheme: GPT"
    else:
        print "Scheme: Unknown"

    print "Partitions:"
    r.list_partitions()