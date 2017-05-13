# -*- coding: utf-8 -*-
from rawdisk.util.rawstruct import RawStruct
from .headers import MBR_PARTITION_ENTRY


MBR_SIGNATURE = 0xAA55
MBR_SIG_SIZE = 2
MBR_SIG_OFFSET = 0x1FE
MBR_SIZE = 512
PT_ENTRY_SIZE = 16
PT_TABLE_OFFSET = 0x1BE
PT_TABLE_SIZE = PT_ENTRY_SIZE * 4
SECTOR_SIZE = 512


class MbrPartitionEntry(RawStruct):
    def __init__(self, data):
        RawStruct.__init__(self, data)

        tmp = self.get_ubyte(2)
        tmp2 = self.get_ubyte(6)

        self.fields = MBR_PARTITION_ENTRY(
            self.get_ubyte(0),          # boot indicator
            self.get_ubyte(1),          # starting_head
            tmp & 0x3F,                 # starting_sector
            ((tmp & 0xC0) << 2) +
            self.get_ubyte(3),          # starting cylinder
            self.get_ubyte(4),          # part_type
            self.get_ubyte(5),          # ending_head
            tmp2 & 0x3F,                # ending_sector
            ((tmp2 & 0xC0) << 2) +
            self.get_ubyte(7),      # ending cylinder
            self.get_uint_le(8),        # relative sector
            self.get_uint_le(12),       # total sectors
        )

    @property
    def part_offset(self):
        return SECTOR_SIZE * self.fields.relative_sector

    @property
    def part_type(self):
        return self.fields.part_type


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
            entry = MbrPartitionEntry(
                self.get_chunk(PT_ENTRY_SIZE * i, PT_ENTRY_SIZE)
            )

            if (entry.fields.part_type != 0):
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

        if signature != MBR_SIGNATURE:
            raise Exception("Invalid MBR signature")

        if load_partition_table:
            self._load_partition_table()

    def export_bootstrap(self, filename):
        self.export(filename, 0, 446)

    def _load_partition_table(self):
        self.partition_table = PartitionTable(
            self.get_chunk(PT_TABLE_OFFSET, PT_TABLE_SIZE)
        )
