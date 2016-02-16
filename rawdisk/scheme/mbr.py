# -*- coding: utf-8 -*-


from rawdisk.util.rawstruct import RawStruct


MBR_SIGNATURE = 0xAA55
MBR_SIG_SIZE = 2
MBR_SIG_OFFSET = 0x1FE
MBR_SIZE = 512
PT_ENTRY_SIZE = 16
PT_TABLE_OFFSET = 0x1BE
PT_TABLE_SIZE = PT_ENTRY_SIZE * 4
SECTOR_SIZE = 512

DEFAULT_GEOMETRY = {
  'HPC': 255, # heads per cylinder
  'SPT': 63,  # sectors per track
}

TYPES = {
  0x0C: 'fat32_lba',
  0x83: 'linux',
}

class PartitionEntry(RawStruct):
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
    def __init__(self, data):
        RawStruct.__init__(self, data)

        self.boot_indicator = self.get_uchar(0)
        self.starting_head = self.get_uchar(1)
        tmp = self.get_uchar(2)
        self.starting_sector = tmp & 0x3F   # Only bits 0-5 are used
        self.starting_cylinder = ((tmp & 0xC0) << 2) + \
            self.get_uchar(3)
        self.part_type = self.get_uchar(4)
        self.ending_head = self.get_uchar(5)

        tmp = self.get_uchar(6)
        self.ending_sector = tmp & 0x3F
        self.ending_cylinder = ((tmp & 0xC0) << 2) + \
            self.get_uchar(7)
        self.relative_sector = self.get_uint_le(8)
        self.total_sectors = self.get_uint_le(12)
        self.part_offset = SECTOR_SIZE*self.relative_sector

    def chs2lba(self, cyl, head, sect, geometry=DEFAULT_GEOMETRY):
        """ helper for consistency check """
        hpc, spt = geometry['HPC'], geometry['SPT']
        return sect-1 + head*spt + cyl*hpc*spt

    def get_type_label(self):
        if self.part_type in TYPES:
            return '%s' % TYPES[self.part_type]
        else:
            return 'unknown'

    def __str__(self):
        # calculated values
        fields = self.__dict__.copy()
        fields['chs_start_sector'] = self.chs2lba(
            self.starting_cylinder,
            self.starting_head,
            self.starting_sector)
        fields['chs_end_sector'] = self.chs2lba(
            self.ending_cylinder,
            self.ending_head,
            self.ending_sector)
        fields['lba_start_sector'] = self.relative_sector
        fields['lba_end_sector'] = (self.relative_sector
            + self.total_sectors - 1)

        fields['label'] = '(%s)' % self.get_type_label()

        return """\
Bootable: %(boot_indicator)s
Type: 0x%(part_type)02X %(label)s
Start (CHS): %(chs_start_sector)s
End   (CHS): %(chs_end_sector)s
Start (LBA): %(lba_start_sector)s
End   (LBA): %(lba_end_sector)s
""" % fields


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
            entry = PartitionEntry(
                self.get_chunk(PT_ENTRY_SIZE * i, PT_ENTRY_SIZE)
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
    def _load_partition_table(self):
        self.partition_table = PartitionTable(
            self.get_chunk(PT_TABLE_OFFSET, PT_TABLE_SIZE)
        )

    def __init__(self, filename=None, load_partition_table=True):
        RawStruct.__init__(
            self,
            filename=filename,
            length=MBR_SIZE
        )

        signature = self.get_ushort_le(MBR_SIG_OFFSET)

        if (signature != MBR_SIGNATURE):
            raise Exception("Invalid MBR signature")

        if (load_partition_table):
            self._load_partition_table()
