# -*- coding: utf-8 -*-


from rawdisk.filesystems.volume import Volume
import logging


class EfiSystemVolume(Volume):
    """Structure for EFI System volume
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.fd = None

    def load(self, filename, offset):
        """Will eventually load information for Apple_Boot volume. \
        Not yet implemented"""
        try:
            self.offset = offset
            # self.fd = open(filename, 'rb')
            # self.fd.close()
        except IOError:
            self.logger.error('Unable to load EfiSystem volume')

    def dump_volume(self):
        print("TODO")

    def __str__(self):
        return "Type: EFI System, Offset: 0x%X" % (
            self.offset
        )
