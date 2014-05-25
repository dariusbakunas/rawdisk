from bpb import *
from rawdisk.util.rawstruct import RawStruct

BPB_SIZE = 25
BPB_OFFSET = 0x0B
EXTENDED_BPB_SIZE = 48

class BootSector(RawStruct):
    def __init__(self, data = None):
        RawStruct.data.fset(self, data)
        self.oem_id = self.get_string(3, 8)
        self.bpb = Bpb(self.get_chunk(BPB_OFFSET, BPB_SIZE + EXTENDED_BPB_SIZE))
        self.mft_offset = self.bpb.bytes_per_sector * \
            self.bpb.sectors_per_cluster * self.bpb.mft_cluster