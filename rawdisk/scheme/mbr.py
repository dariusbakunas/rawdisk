# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2014 Darius Bakunas

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from rawdisk.util.rawstruct import RawStruct


MBR_SIGNATURE = 0xAA55
MBR_SIG_SIZE = 2
MBR_SIG_OFFSET = 0x1FE
MBR_SIZE = 512
PT_ENTRY_SIZE = 16
PT_TABLE_OFFSET = 0x1BE
PT_TABLE_SIZE = PT_ENTRY_SIZE * 4
SECTOR_SIZE = 512


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
        self.boot_indicator = self.get_ubyte(0)
        self.starting_head = self.get_ubyte(1)
        tmp = self.get_ubyte(2)
        self.starting_sector = tmp & 0x3F   # Only bits 0-5 are used
        self.starting_cylinder = ((tmp & 0xC0) << 2) + \
            self.get_ubyte(3)
        self.part_type = self.get_ubyte(4)
        self.ending_head = self.get_ubyte(5)

        tmp = self.get_ubyte(6)
        self.ending_sector = tmp & 0x3F
        self.ending_cylinder = ((tmp & 0xC0) << 2) + \
            self.get_ubyte(7)
        self.relative_sector = self.get_uint(8)
        self.total_sectors = self.get_uint(12)
        self.part_offset = SECTOR_SIZE*self.relative_sector


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

    Attributes:
        partition_table (PartitionTable): Initialized \
        :class:`PartitionTable` object
    """
    def __init__(self):
        RawStruct.__init__(self)
        self.partition_table = None

    def load(self, filename):
        """Reads master boot record of the filesystem and
        loads partition table entries

        Args:
            filename (str): path to file or device to open for reading

        Raises:
            IOError: If file does not exist or is not readable.
            Exception: If source has invalid MBR signature
        """
        with open(filename, 'rb') as f:
            # Verify MBR signature first
            self.load_from_source(f, 0, MBR_SIZE)
            signature = self.get_ushort(MBR_SIG_OFFSET)

            if (signature != MBR_SIGNATURE):
                raise Exception("Invalid MBR signature")

            self.partition_table = PartitionTable(
                self.get_chunk(PT_TABLE_OFFSET, PT_TABLE_SIZE)
            )
