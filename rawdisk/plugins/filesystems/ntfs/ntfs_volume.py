import hurry.filesize
from mft import *
from bootsector import *
from rawdisk.filesystems.volume import Volume

NTFS_BOOTSECTOR_SIZE = 512


class NtfsVolume(Volume):
    def __init__(self):
        self.offset = 0
        self.bootsector = None
        self.mft_table = None
        self.fd = None

    def load(self, filename, offset):
        try:
            self.offset = offset 
            self.fd = open(filename, 'rb')
            self.load_bootsector()
            self.load_mft_table()
            self.fd.close()
        except IOError, e:
            print e

    def load_bootsector(self):
        self.fd.seek(self.offset)
        data = self.fd.read(NTFS_BOOTSECTOR_SIZE)
        self.bootsector = BootSector(data)

    def load_mft_table(self):
        self.mft_table = MftTable(self.mft_table_offset)
        self.mft_table.load(self.fd)

    def __str__(self):
        return "Type: NTFS, Offset: 0x%X, Size: %s, MFT Table Offset: 0x%X" % (
            self.offset,
            hurry.filesize.size(self.size),
            self.mft_table_offset
        )

    @property
    def size(self):
        return self.bootsector.bpb.bytes_per_sector * \
            self.bootsector.bpb.total_sectors

    @property
    def mft_table_offset(self):
        return self.offset + self.bootsector.mft_offset
