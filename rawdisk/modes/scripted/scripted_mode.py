import logging
from rawdisk import scheme
from rawdisk.session import Session
from rawdisk.plugins.plugin_manager import PluginManager
from ..mode import Mode


class ScriptedMode(Mode):
    @staticmethod
    def entry(args=None):
        logger = logging.getLogger(__name__)

        session = Session()
        session.load_plugins()

        if args is None or args.filename is None:
            logger.error('-f FILENAME must be specified')
            exit(0)

        try:
            session.load(args.filename)
        except IOError:
            logger.error(
                'Failed to open disk image file: {}'.format(args.filename))

        if session.partition_scheme == scheme.common.SCHEME_MBR:
            print('Scheme: MBR')
        elif session.partition_scheme == scheme.common.SCHEME_GPT:
            print('Scheme: GPT')
        else:
            print('Scheme: Unknown')

        print('Partitions:')
        session.volumes()
