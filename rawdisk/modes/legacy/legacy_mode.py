import logging
from rawdisk import scheme, reader
from ..mode import Mode

class LegacyMode(Mode):
    @staticmethod
    def entry(args):
        logger = logging.getLogger(__name__)

        r = reader.Reader()
        r.load_plugins()

        if args.filename is None:
            logger.error('-f FILENAME must be specified')

        try:
            r.load(args.filename)
        except IOError:
            logger.error(
                'Failed to open disk image file: {}'.format(args.filename))

        if r.scheme == scheme.common.SCHEME_MBR:
            print('Scheme: MBR')
        elif r.scheme == scheme.common.SCHEME_GPT:
            print('Scheme: GPT')
        else:
            print('Scheme: Unknown')

        print('Partitions:')
        r.list_partitions()
