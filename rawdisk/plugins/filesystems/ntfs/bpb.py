# -*- coding: utf-8 -*-

from headers import BIOS_PARAMETER_BLOCK
from rawdisk.util.rawstruct import RawStruct

BPB_SIZE = 25
BPB_OFFSET = 0x0B
EXTENDED_BPB_SIZE = 48


class Bpb(RawStruct):
    """Bios parameter block.

    Attributes:
        bytes_per_sector (ushort): Sector size with which the physical \
        disc medium has been low-level formatted in bytes.
        sectors_per_cluster (ubyte): Number of sectors in an allocation unit.
        reserved_sectors (ushort): Number of sectors in the area at the start \
        of the volume that is reserved for operating system boot code.
        media_descriptor (ubyte): Describes type of device used eg. floppy,
        harddisk (not used anymore?).
        total_sectors (ulonglong): Total number of sectors in the volume.
        mft_cluster (ulonglong): MFT table first cluster number \
        (*mft offset = volume offset + bytes_per_sector * \
            sectors_per_cluster * mft_cluster*).
        mft_mirror_cluster (ulonglong): Mirror MFT table cluster number.
        clusters_per_mft (signed char): MFT record size. \
        Per Microsoft: If this number is positive (up to 0x7F), it represents \
        Clusters per MFT record. If the number is negative (0x80 to 0xFF), \
        the size of the File Record is 2 raised to the absolute value of \
        this number.
        clusters_per_index (uint): Index block size.
        volume_serial (ulonglong): Volume serial number.
        checksum (uint): BPB checksum.

    See More:
        | http://en.wikipedia.org/wiki/BIOS_parameter_block
        | http://ntfs.com/ntfs-partition-boot-sector.htm
        | http://homepage.ntlworld.com\
/jonathan.deboynepollard/FGA/bios-parameter-block.html
    """

    def __init__(
        self,
        data=None,
        offset=None,
        filename=None
    ):

        RawStruct.__init__(
            self,
            data=data,
            offset=offset,
            length=BPB_SIZE + EXTENDED_BPB_SIZE,
            filename=filename
        )

        self.info = BIOS_PARAMETER_BLOCK(
                self.get_ushort_le(0),
                self.get_uchar(2),
                self.get_ushort_le(3),
                self.get_uchar(10),
                self.get_ushort_le(13),
                self.get_ushort_le(15),
                self.get_uint_le(17),
                self.get_ulonglong_le(29),
            )

        self.mft_cluster = self.get_ulonglong_le(37)
        self.mft_mirror_cluster = self.get_ulonglong_le(45)
        self.clusters_per_mft = self.get_char(53)
        self.clusters_per_index = self.get_uchar(57)
        self.volume_serial = self.get_ulonglong_le(58)
        self.checksum = self.get_uint_le(66)

    @property
    def total_clusters(self):
        return self.info.total_sectors / self.info.sectors_per_cluster

    @property
    def bytes_per_cluster(self):
        return self.info.sectors_per_cluster * self.info.bytes_per_sector

    @property
    def volume_size(self):
        """Returns volume size in bytes"""
        return self.info.bytes_per_sector * self.info.total_sectors

    @property
    def mft_record_size(self):
        """
        Returns:
            int: MFT record size in bytes
        """
        if (self.clusters_per_mft < 0):
            return 2 ** abs(self.clusters_per_mft)
        else:
            return self.clusters_per_mft * self.sectors_per_cluster * \
                self.bytes_per_sector

    @property
    def mft_offset(self):
        """
        Returns:
            int: MFT Table offset from the beginning of the partition in bytes
        """
        return self.info.bytes_per_sector * \
            self.info.sectors_per_cluster * self.mft_cluster

    @property
    def mft_mirror_offset(self):
        """
        Returns:
            int: Mirror MFT Table offset from the beginning of the partition \
            in bytes
        """
        return self.info.bytes_per_sector * \
            self.info.sectors_per_cluster * self.mft_mirror_cluster
