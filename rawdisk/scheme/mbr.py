# -*- coding: utf-8 -*-
from rawdisk.util.rawstruct import RawStruct
from headers import MBR_PARTITION_ENTRY


MBR_SIGNATURE = 0xAA55
MBR_SIG_SIZE = 2
MBR_SIG_OFFSET = 0x1FE
MBR_SIZE = 512
PT_ENTRY_SIZE = 16
PT_TABLE_OFFSET = 0x1BE
PT_TABLE_SIZE = PT_ENTRY_SIZE * 4
SECTOR_SIZE = 512


class PartitionTable(RawStruct):
    """Represents MBR partition table.

    Args:
        data (str): byte array to initialize structure with.

    Attributes:
        entries (list): List of initialized :class:`PartitionEntry` objects
    """
    def __init__(self, data):
        RawStruct.__init__(self, data)
        self.entries = []

        for i in range(0, 4):
            offset = PT_ENTRY_SIZE * i
            tmp = self.get_ubyte(offset + 2)
            tmp2 = self.get_ubyte(offset + 6)
            relative_sector = self.get_uint_le(offset + 8)

            entry = MBR_PARTITION_ENTRY(
                self.get_ubyte(offset),             # boot_indicator
                self.get_ubyte(offset + 1),         # starting_head
                tmp & 0x3F,                         # starting_sector
                # starting_cylinder
                ((tmp & 0xC0) << 2) + self.get_ubyte(offset + 3),
                self.get_ubyte(offset + 4),         # part_type
                self.get_ubyte(offset + 5),         # ending_head
                tmp2 & 0x3F,                        # ending_sector
                # ending_cylinder
                ((tmp2 & 0xC0) << 2) + self.get_ubyte(offset + 7),
                relative_sector,                    # relative_sector
                self.get_uint_le(offset + 12),      # total_sectors
                SECTOR_SIZE * relative_sector       # part_offset
            )

            if (entry.part_type != 0):
                self.entries.append(entry)


class Mbr(RawStruct):
    """Represents the Master Boot Record of the filesystem.

    Args:
        filename (str): path to file or device to open for reading

    Attributes:
        partition_table (PartitionTable): Initialized \
        :class:`PartitionTable` object

    Raises:
        IOError: If file does not exist or is not readable.
        Exception: If source has invalid MBR signature
    """

    def __init__(self, filename=None, load_partition_table=True):
        RawStruct.__init__(
            self,
            filename=filename,
            length=MBR_SIZE
        )

        self.bootstrap = self.get_chunk(0, 446)
        signature = self.get_ushort_le(MBR_SIG_OFFSET)

        if (signature != MBR_SIGNATURE):
            raise Exception("Invalid MBR signature")

        if (load_partition_table):
            self._load_partition_table()

    def export_bootstrap(self, filename):
        self.export(filename, 0, 446)

    def _load_partition_table(self):
        self.partition_table = PartitionTable(
            self.get_chunk(PT_TABLE_OFFSET, PT_TABLE_SIZE)
        )
