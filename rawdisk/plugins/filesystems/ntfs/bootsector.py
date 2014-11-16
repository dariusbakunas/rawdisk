# -*- coding: utf-8 -*-


from bpb import Bpb, BPB_OFFSET, BPB_SIZE, EXTENDED_BPB_SIZE
from rawdisk.util.rawstruct import RawStruct


class BootSector(RawStruct):
    """Represents NTFS Bootsector

    Attributes:
        oem_id (8 byte string): NTFS filesystem signature 'NTFS    '
        bpb (Bpb): Initialized :class:`~.bpb.Bpb` object.
        mft_offset (int): Offset to MFT table from the start of \
        NTFS volume in bytes

    See More:
        http://ntfs.com/ntfs-partition-boot-sector.htm
    """
    def __init__(self, data=None, offset=None, length=None, filename=None):
        RawStruct.__init__(
            self,
            data=data,
            offset=offset,
            length=length,
            filename=filename
        )

        self.oem_id = self.get_string(3, 8)
        self.bpb = Bpb(self.get_chunk(
            BPB_OFFSET, BPB_SIZE + EXTENDED_BPB_SIZE))
