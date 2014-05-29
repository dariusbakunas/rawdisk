# Copyright (c) 2009, David Buxton <david@gasmark6.com>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import rawdisk.filesystems
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
        boot_indicator (ubyte): Boot indicator bit flag: 0 = no, 0x80 = bootable (or "active")
        starting_head (ubyte): Starting head for the partition
        starting_sector (6 bits): Starting sector for the partition
        starting_cylinder (10 bits): Starting cylinder for the partition
        part_type (ubyte): Partition type id
        ending_head (ubyte): Ending head of the partition
        ending_sector (6 bits): Ending sector
        ending_cylinder (10 bits): Ending cylinder
        relative_sector (uint): The offset from the beginning of the disk to the beginning \
        of the volume, counting by sectors.
        total_sectors (uint): The total number of sectors in the volume.
        part_offset (uint): The offset from the beginning of the disk to the beginning \
        of the volume, counting by bytes.

    See Also:
        | MBR Table (http://technet.microsoft.com/en-us/library/cc976786.aspx)
        | MBR Partition Types (http://en.wikipedia.org/wiki/Partition_type#List_of_partition_IDs)
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
        partition_table (PartitionTable): Initialized :class:`PartitionTable` object
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
