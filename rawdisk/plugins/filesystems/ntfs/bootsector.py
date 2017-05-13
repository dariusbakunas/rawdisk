# -*- coding: utf-8 -*-


from rawdisk.util.rawstruct import RawStruct
from .headers import BIOS_PARAMETER_BLOCK, EXTENDED_BIOS_PARAMETER_BLOCK


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
            self.get_ushort_le(0x0B),       # bytes_per_sector
            self.get_ubyte(0x0D),           # sectors_per_cluster
            self.get_ushort_le(0x0E),       # reserved_sectors
            self.get_ubyte(0x15),           # media_type
            self.get_ushort_le(0x18),       # sectors_per_track
            self.get_ushort_le(0x1A),       # heads
            self.get_uint_le(0x1C),         # hidden_sectors
            self.get_ulonglong_le(0x28),    # total sectors
        )

        self.extended_bpb = EXTENDED_BIOS_PARAMETER_BLOCK(
            self.get_ulonglong_le(0x30),    # mft_cluster
            self.get_ulonglong_le(0x38),    # mft_mirror_cluster
            self.get_byte(0x40),            # clusters_per_mft
            self.get_ubyte(0x44),           # clusters_per_index
            self.get_ulonglong_le(0x48),    # volume_serial
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
        return int(self.bpb.total_sectors / self.bpb.sectors_per_cluster)

    @property
    def bytes_per_cluster(self):
        return self.bpb.sectors_per_cluster * self.bpb.bytes_per_sector

    @property
    def volume_size(self):
        """Returns volume size in bytes"""
        return self.bpb.bytes_per_sector * self.bpb.total_sectors
