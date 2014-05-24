from rawdisk.filesystems.volume import Volume
from rawdisk.util.rawstruct import RawStruct
import hurry.filesize

VOLUME_HEADER_OFFSET = 1024


class VolumeHeader(RawStruct):
    def __init__(self, data):
        RawStruct.__init__(self, data)
        self.signature = self.get_string(0x00,2)
        # HFS+ everything is stored in big-endian
        self.version = self.get_ushort(0x02, True)
        self.attributes = self.get_uint(0x04, True)

class HfsPlusVolume(Volume):
    def __init__(self):
        self.fd = None
        self.vol_header = None

    def mount(self, filename, offset):
        try:
            self.offset = offset 
            self.fd = open(filename, 'rb')
            # 1024 - temporary, need to find out actual volume header size
            self.fd.seek(self.offset + VOLUME_HEADER_OFFSET)
            data = self.fd.read(1024)
            self.vol_header = VolumeHeader(data)
        except IOError, e:
            print e

    def unmount(self):
        try:
            if not self.fd.closed:
                self.fd.close()
        except IOError, e:
            print e

    def is_mounted(self):
        if (self.fd != None and not self.fd.closed):
            return True
        else:
            return False

    def __str__(self):
        return "Type: HFS+, Offset: 0x%X" % (
            self.offset
        )
