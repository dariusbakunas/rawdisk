from rawdisk.filesystems.common import Partition
from rawdisk.util.rawstruct import RawStruct
import hurry.filesize

BPB_SIZE = 25
BPB_OFFSET = 0x0B
EXTENDED_BPB_SIZE = 48


class NTFS_Boot_Sector(RawStruct):
    def __init__(self):
        self.bpb = BPB()

    def load(self, data):
        RawStruct.data.fset(self, data)
        self.oem_id = self.get_string(3, 8)
        self.bpb.load(self.get_chunk(BPB_OFFSET, BPB_SIZE + EXTENDED_BPB_SIZE))


class Master_File_Table:
    pass


class BPB(RawStruct):
    """Bios parameter block
    """
    def __init__(self):
        pass

    def load(self, data):
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


class NTFS_Partition(Partition):
    def __init__(self):
        Partition.__init__(self)
        self.bootsector = NTFS_Boot_Sector()

    def load(self, filename, offset):
        try:
            with open(filename, 'rb') as f:
                f.seek(offset)
                data = f.read(512)
                self.bootsector.load(data)

        except IOError, e:
            print e