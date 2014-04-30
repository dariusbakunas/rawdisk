from optparse import OptionParser
import os
import sys


def main():
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

if __name__ == "__main__":
    main()