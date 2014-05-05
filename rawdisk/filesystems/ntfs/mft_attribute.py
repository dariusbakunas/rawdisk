import hexdump
from rawdisk.util.rawstruct import RawStruct

MFT_ATTR_HEADER_SIZE = 16


class MftAttrHeader(RawStruct):
    def __init__(self, data):
        RawStruct.data.fset(self, data)
        self.type = self.get_uint(0)
        self.length = self.get_uint(4)
        self.non_resident_flag = self.get_ubyte(8)
        self.length_of_name = self.get_ubyte(9) # Used only for ADS
        self.offset_to_name = self.get_ushort(10) # Used only for ADS
        self.flags = self.get_ushort(12) # Flags (Compressed, Encrypted, Sparse)
        self.identifier = self.get_ushort(14)


class MftAttr(RawStruct):
    def __init__(self, data):
        RawStruct.data.fset(self, data)
        self.header = MftAttributeHeader(
            self.get_chunk(0, MFT_ATTR_HEADER_SIZE)
        )
