# -*- coding: utf-8 -*-


from rawdisk.util.rawstruct import RawStruct
from headers import BIOS_PARAMETER_BLOCK, EXTENDED_BIOS_PARAMETER_BLOCK


BPB_OFFSET = 0x0B

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

        self.bpb = BIOS_PARAMETER_BLOCK(
                self.get_ushort_le(0x0B),
                self.get_uchar(BPB_OFFSET + 2),
                self.get_ushort_le(BPB_OFFSET + 3),
                self.get_uchar(BPB_OFFSET + 10),
                self.get_ushort_le(BPB_OFFSET + 13),
                self.get_ushort_le(BPB_OFFSET + 15),
                self.get_uint_le(BPB_OFFSET + 17),
                self.get_ulonglong_le(BPB_OFFSET + 29),
            )

        self.extended_bpb = EXTENDED_BIOS_PARAMETER_BLOCK(
                self.get_ulonglong_le(BPB_OFFSET + 37),
                self.get_ulonglong_le(BPB_OFFSET + 45),
                self.get_char(BPB_OFFSET + 53),
                self.get_uchar(BPB_OFFSET + 57),
                self.get_ulonglong_le(BPB_OFFSET + 58),
                self.get_uint_le(BPB_OFFSET + 66)
            )

    @property
    def mft_record_size(self):
        """
        Returns:
            int: MFT record size in bytes
        """
        if (self.extended_bpb.clusters_per_mft < 0):
            return 2 ** abs(self.extended_bpb.clusters_per_mft)
        else:
            return self.clusters_per_mft * self.sectors_per_cluster * \
                self.bytes_per_sector

    @property
    def mft_offset(self):
        """
        Returns:
            int: MFT Table offset from the beginning of the partition in bytes
        """
        return self.bpb.bytes_per_sector * \
            self.bpb.sectors_per_cluster * self.extended_bpb.mft_cluster

    @property
    def mft_mirror_offset(self):
        """
        Returns:
            int: Mirror MFT Table offset from the beginning of the partition \
            in bytes
        """
        return self.bpb.bytes_per_sector * \
            self.bpb.sectors_per_cluster * self.extended_bpb.mft_mirror_cluster

    @property
    def total_clusters(self):
        return self.bpb.total_sectors / self.bpb.sectors_per_cluster

    @property
    def bytes_per_cluster(self):
        return self.bpb.sectors_per_cluster * self.bpb.bytes_per_sector

    @property
    def volume_size(self):
        """Returns volume size in bytes"""
        return self.bpb.bytes_per_sector * self.bpb.total_sectors

        #self.bpb = Bpb(self.get_chunk(
         #   BPB_OFFSET, BPB_SIZE + EXTENDED_BPB_SIZE))
