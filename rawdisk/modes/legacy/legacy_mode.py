import logging
from rawdisk import scheme
from rawdisk.session import Session
from rawdisk.plugins.manager import Manager
from ..mode import Mode


class LegacyMode(Mode):
    @staticmethod
    def entry(args=None):
        logger = logging.getLogger(__name__)

        s = Session(plugin_manager=Manager())
        s.load_plugins()

        if args is None or args.filename is None:
            logger.error('-f FILENAME must be specified')

        try:
            s.load(args.filename)
        except IOError:
            logger.error(
                'Failed to open disk image file: {}'.format(args.filename))

        if s.scheme == scheme.common.SCHEME_MBR:
            print('Scheme: MBR')
        elif s.scheme == scheme.common.SCHEME_GPT:
            print('Scheme: GPT')
        else:
            print('Scheme: Unknown')

        print('Partitions:')
        s.list_partitions()
