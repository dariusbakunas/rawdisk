# -*- coding: utf-8 -*-


from rawdisk.filesystems.volume import Volume


class AppleBootVolume(Volume):
    """Structure for Apple_Boot volume
    """
    def __init__(self):
        self.fd = None

    def load(self, filename, offset):
        """Will eventually load information for Apple_Boot volume.
        Not yet implemented"""
        try:
            self.offset = offset
            # self.fd = open(filename, 'rb')
            # self.fd.close()
        except IOError as e:
            print(e)

    def dump_volume(self):
        print("TODO")

    def __str__(self):
        return "Type: Apple_Boot, Offset: 0x%X" % (
            self.offset
        )
