# -*- coding: utf-8 -*-
from rawdisk.util.rawstruct import RawStruct
from .headers import MBR_PARTITION_ENTRY
import logging


MBR_SIGNATURE = 0xAA55
MBR_SIG_SIZE = 2
MBR_SIG_OFFSET = 0x1FE
MBR_SIZE = 512
MBR_NUM_PARTS = 4
PARTITION_ENTRY_SIZE = 16
PARTITION_TABLE_OFFSET = 0x1BE
PARTITION_TABLE_SIZE = PARTITION_ENTRY_SIZE * MBR_NUM_PARTS
SECTOR_SIZE = 512

DEFAULT_GEOMETRY = {
  'HPC': 255, # heads per cylinder
  'SPT': 63,  # sectors per track
}

TYPES = {
  0x0C: 'fat32_lba',
  0x83: 'linux',
}

logger = logging.getLogger(__name__)

class MbrPartitionEntry(RawStruct):
    def __init__(self, data):
        RawStruct.__init__(self, data)

        tmp = self.get_ubyte(2)
        tmp2 = self.get_ubyte(6)

        self.fields = MBR_PARTITION_ENTRY(
            self.get_ubyte(0),          # boot_indicator
            self.get_ubyte(1),          # starting_head
            tmp & 0x3F,                 # starting_sector
            ((tmp & 0xC0) << 2) +
              self.get_ubyte(3),        # starting_cylinder
            self.get_ubyte(4),          # part_type
            self.get_ubyte(5),          # ending_head
            tmp2 & 0x3F,                # ending_sector
            ((tmp2 & 0xC0) << 2) +
              self.get_ubyte(7),        # ending_cylinder
            self.get_uint_le(8),        # relative_sector
            self.get_uint_le(12),       # total_sectors
        )

    @property
    def part_offset(self):
        return SECTOR_SIZE * self.fields.relative_sector

    @property
    def part_type(self):
        return self.fields.part_type

    def chs2lba(self, cyl, head, sect, geometry=DEFAULT_GEOMETRY):
        """ helper for consistency check """
        hpc, spt = geometry['HPC'], geometry['SPT']
        return sect-1 + head*spt + cyl*hpc*spt

    @property
    def type_label(self):
        if self.fields.part_type in TYPES:
            return str(TYPES[self.fields.part_type])
        else:
            return 'unknown'

    def __str__(self):
        # calculated values
        fields = {'self': self}
        fields['chs_start_sector'] = self.chs2lba(
            self.fields.starting_cylinder,
            self.fields.starting_head,
            self.fields.starting_sector)
        fields['chs_end_sector'] = self.chs2lba(
            self.fields.ending_cylinder,
            self.fields.ending_head,
            self.fields.ending_sector)
        fields['lba_start_sector'] = self.fields.relative_sector
        fields['lba_end_sector'] = (self.fields.relative_sector
            + self.fields.total_sectors - 1)
        return """\
Bootable: {self.fields.boot_indicator}
Type: {self.part_type:02X} ({self.type_label})
Start-End (by CHS): {chs_start_sector}-{chs_end_sector}
Start-End (by LBA): {lba_start_sector}-{lba_end_sector}
""".format(**fields)


class PartitionTable(RawStruct):
    """Represents MBR partition table.

    Args:
        data (bytes): byte array to initialize structure with.

    Attributes:
        entries (list): List of initialized :class:`PartitionEntry` objects
    """
    def __init__(self, data):
        RawStruct.__init__(self, data)
        self.entries = []

        for i in range(0, MBR_NUM_PARTS):
            entry = MbrPartitionEntry(
                self.get_chunk(PARTITION_ENTRY_SIZE * i, PARTITION_ENTRY_SIZE)
            )

            if entry.fields.part_type != 0:
                self.entries.append(entry)

    def __getitem__(self, index):
        return self.entries.__getitem__(index)


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
        logger.info('Loading partition table')
        self.partition_table = PartitionTable(
            self.get_chunk(PARTITION_TABLE_OFFSET, PARTITION_TABLE_SIZE)
        )
