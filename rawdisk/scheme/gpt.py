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

import uuid
import struct
from rawdisk.util.rawstruct import RawStruct

GPT_HEADER_OFFSET = 0x200
GPT_SIG_SIZE = 8
GPT_SIGNATURE = 'EFI PART'


class GptHeader(RawStruct):
    """Represents GUID partition table header (LBA1).

    Args:
        data (str): byte array to initialize structure with. \
        Must be valid gpt header.

    Attributes:
        signature (str): "EFI PART", 45h 46h 49h 20h 50h 41h 52h 54h
        revision (uint): GPT Revision
        header_size (uint): Total length of gpt header
        crc32 (uint): CRC32 of the header
        current_lba (ulonglong): LBA location of this header
        backup_lba (ulonglong): LBA loction of header's copy
        first_usable_lba (ulonglong): First usable LBA for partitions
        last_usable_lba (ulonglong): Last usable LBA for partitions
        disk_guid (uuid): Disk GUID (UUID for Unixes)
        part_lba (ulonglong): Starting LBA of array of partition entries
        num_partitions (uint): Number of partition entries in array
        part_size (uint): Size of a single partition entry (usually 128)
        part_array_crc32 (uint): CRC32 of partition array

    Raises:
        Exception: If signature does not match valid GPT signature

    See Also:
        http://en.wikipedia.org/wiki/GUID_Partition_Table#Partition_table_header_.28LBA_1.29
    """
    def __init__(self, data):
        RawStruct.__init__(self, data)
        self.signature = self.get_string(0, 8)

        if (self.signature != GPT_SIGNATURE):
            raise Exception("Invalid GPT signature")

        self.revision = self.get_uint(0x08)
        self.header_size = self.get_uint(0x0C)
        self.crc32 = self.get_uint(0x10)
        # 4 bytes @0x14 reserved, must be 0
        self.current_lba = self.get_ulonglong(0x18)
        self.backup_lba = self.get_ulonglong(0x20)
        self.first_usable_lba = self.get_ulonglong(0x28)
        self.last_usable_lba = self.get_ulonglong(0x30)
        # Not sure if this is correct
        self.disk_guid = self.get_uuid(0x38)
        self.part_lba = self.get_ulonglong(0x48)
        self.num_partitions = self.get_uint(0x50)
        self.part_size = self.get_uint(0x54)
        self.part_array_crc32 = self.get_uint(0x58)
        # Rest of bytes @ 0x5C must be zeroes (420 for 512 sectors)


class GptPartition(RawStruct):
    """Represents GPT partition entry.

    Args:
        data (str): byte array that belongs to valid GPT partition entry.

    Attributes:
        type_guid (uuid): Partition type GUID
        part_guid (uuid): Unique partition GUID
        first_lba (ulonglong): First LBA of partition
        last_lba (ulonglong): Last LBA of partition
        attr_flags (ulonglong): Attribute flags (e.g. bit 60 denotes read-only)
        name (str): Partition name (36 UTF-16LE code units)

    See Also:
        http://en.wikipedia.org/wiki/GUID_Partition_Table#Partition_entries
    """
    def __init__(self, data):
        RawStruct.__init__(self, data)
        self.type_guid = self.get_uuid(0x00)
        self.part_guid = self.get_uuid(0x10)
        self.first_lba = self.get_ulonglong(0x20)
        self.last_lba = self.get_ulonglong(0x28)
        self.attr_flags = self.get_ulonglong(0x30)
        self.name = self.get_chunk(0x38, 72).decode('utf-16')


class Gpt(object):
    """Represents GPT partition table.

    Attributes:
        partition_entries (list): List of initialized \
        :class:`GptPartition` objects.
        header (GptHeader): Initialized :class:`GptHeader` object
    """
    def __init__(self):
        self.partition_entries = []

    def load(self, filename):
        """Loads GPT partition table.

        Args:
            filename (str): path to file or device to open for reading

        Raises:
            IOError: If file does not exist or not readable
        """
        with open(filename, 'rb') as f:
            self.fd = f
            f.seek(GPT_HEADER_OFFSET + 0x0C)
            header_size = struct.unpack("<I", f.read(4))[0]
            f.seek(GPT_HEADER_OFFSET)
            self.header = GptHeader(f.read(header_size))
            self._load_partition_entries()

    def _load_partition_entries(self, block_size=512):
        """Loads the list of :class:GptPartition partition entries

        Args:
            block_size (uint): Block size of the volume, default: 512
        """

        self.fd.seek(self.header.part_lba * block_size)
        for p in xrange(0, self.header.num_partitions):
            data = self.fd.read(self.header.part_size)
            entry = GptPartition(data)
            if entry.type_guid != uuid.UUID(
                '{00000000-0000-0000-0000-000000000000}'
            ):
                self.partition_entries.append(entry)
