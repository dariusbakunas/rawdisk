from rawdisk.filesystems.common import Volume
from rawdisk.util.rawstruct import RawStruct
import hurry.filesize
from mft import *
import hexdump

BPB_SIZE = 25
BPB_OFFSET = 0x0B
EXTENDED_BPB_SIZE = 48
NTFS_BOOTSECTOR_SIZE = 512


class Bpb(RawStruct):
    """Bios parameter block
    Includes extended BPB
    """
    def __init__(self, data = None):
        RawStruct.data.fset(self, data)
        self.bytes_per_sector = self.get_ushort(0)
        self.sectors_per_cluster = self.get_ubyte(2)
        self.reserved_sectors = self.get_ushort(3)
        self.media_descriptor = self.get_ubyte(10)
        self.sectors_per_track = self.get_ushort(13)
        self.number_of_heads = self.get_ushort(15)
        self.hidden_sectors = self.get_uint(17)
        self.total_sectors = self.get_ulonglong(29)
        self.mft_cluster = self.get_ulonglong(37)
        self.mft_mirror_cluster = self.get_ulonglong(45)
        self.clusters_per_mft = self.get_uint(53)
        self.clusters_per_index = self.get_ubyte(57)
        self.volume_serial = self.get_ulonglong(58)
        self.checksum = self.get_uint(66)


class NtfsBootSector(RawStruct):
    def __init__(self, data = None):
        RawStruct.data.fset(self, data)
        self.oem_id = self.get_string(3, 8)
        self.bpb = Bpb(self.get_chunk(BPB_OFFSET, BPB_SIZE + EXTENDED_BPB_SIZE))
        self.mft_offset = self.bpb.bytes_per_sector * \
            self.bpb.sectors_per_cluster * self.bpb.mft_cluster


class NtfsVolume(Volume):
    def __init__(self):
        self.offset = 0
        self.bootsector = None
        self.mft_table = None
        self.fd = None

    def mount(self, filename, offset):
        try:
            self.offset = offset 
            self.fd = open(filename, 'rb')
            self.load_bootsector()
            self.load_mft_table()
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

    def load_bootsector(self):
        self.fd.seek(self.offset)
        data = self.fd.read(NTFS_BOOTSECTOR_SIZE)
        self.bootsector = NtfsBootSector(data)

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
