# -*- coding: utf-8 -*-
from ctypes import Structure, c_ushort, c_ubyte, c_uint, c_ulonglong, \
    c_byte, c_char


class MBR_PARTITION_ENTRY(Structure):
    """Represents MBR partition entry

    Args:
        data (str): byte array to initialize structure with.

    Attributes:
        boot_indicator (ubyte): Boot indicator bit flag: 0 = no, 0x80 = \
        bootable (or "active")
        starting_head (ubyte): Starting head for the partition
        starting_sector (6 bits): Starting sector for the partition
        starting_cylinder (10 bits): Starting cylinder for the partition
        part_type (ubyte): Partition type id
        ending_head (ubyte): Ending head of the partition
        ending_sector (6 bits): Ending sector
        ending_cylinder (10 bits): Ending cylinder
        relative_sector (uint): The offset from the beginning of the disk to \
        the beginning of the volume, counting by sectors.
        total_sectors (uint): The total number of sectors in the volume.
        part_offset (uint): The offset from the beginning of the disk \
        to the beginning of the volume, counting by bytes.

    See Also:
        | MBR Table (http://technet.microsoft.com/en-us/library/cc976786.aspx)
        | MBR Partition Types \
        (http://en.wikipedia.org/wiki/Partition_type#List_of_partition_IDs)
    """
    _fields_ = [
        ("boot_indicator",          c_ubyte),
        ("starting_head",           c_ubyte),
        ("starting_sector",         c_ubyte),
        ("starting_cylinder",       c_ubyte),
        ("part_type",               c_ubyte),
        ("ending_head",             c_ubyte),
        ("ending_sector",           c_ubyte),
        ("ending_cylinder",         c_ubyte),
        ("relative_sector",         c_ubyte),
        ("total_sectors",           c_uint),
        ("part_offset",             c_uint),
    ]
