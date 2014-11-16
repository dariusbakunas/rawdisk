# -*- coding: utf-8 -*-


from rawdisk.filesystems.volume import Volume


class EfiSystemVolume(Volume):
    """Structure for EFI System volume
    """
    def __init__(self):
        self.fd = None

    def load(self, filename, offset):
        """Will eventually load information for Apple_Boot volume. \
        Not yet implemented"""
        try:
            self.offset = offset
            # self.fd = open(filename, 'rb')
            # self.fd.close()
        except IOError, e:
            print e

    def __str__(self):
        return "Type: EFI System, Offset: 0x%X" % (
            self.offset
        )
