from rawdisk.filesystems.volume import Volume
from rawdisk.util.rawstruct import RawStruct
import hurry.filesize


class AppleBootVolume(Volume):
    def __init__(self):
        self.fd = None

    def load(self, filename, offset):
        try:
            self.offset = offset 
            # self.fd = open(filename, 'rb')
            # self.fd.close()
        except IOError, e:
            print e

    def __str__(self):
        return "Type: Apple_Boot, Offset: 0x%X" % (
            self.offset
        )