# -*- coding: utf-8 -*-


import uuid
import struct
from rawdisk.util.rawstruct import RawStruct
from headers import GPT_HEADER
from ctypes import c_ubyte
import hexdump

GPT_HEADER_OFFSET = 0x200
GPT_SIG_SIZE = 8
GPT_SIGNATURE = 'EFI PART'


class GptHeader(RawStruct):
    def __init__(self, data):
        RawStruct.__init__(self, data)

        self.fields = GPT_HEADER(
            self.get_string(0, 8),              # signature
            self.get_uint_le(0x08),             # revsion
            self.get_uint_le(0x0C),             # header_size
            self.get_uint_le(0x10),             # crc32
            self.get_ulonglong_le(0x18),        # current_lba
            self.get_ulonglong_le(0x20),        # backup_lba
            self.get_ulonglong_le(0x28),        # first_usable_lba
            self.get_ulonglong_le(0x30),        # last_usable_lba
            (c_ubyte * 16).from_buffer_copy(    # disk_guid
                self.get_chunk(0x38, 16)),
            self.get_ulonglong_le(0x48),        # part_lba
            self.get_uint_le(0x50),             # num_partitions
            self.get_uint_le(0x54),             # part_size
            self.get_uint_le(0x58)              # part_array_crc32
        )


class GptPartitionEntry(RawStruct):
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
        self.type_guid = self.get_uuid_le(0x00)
        self.part_guid = self.get_uuid_le(0x10)
        self.first_lba = self.get_ulonglong_le(0x20)
        self.last_lba = self.get_ulonglong_le(0x28)
        self.attr_flags = self.get_ulonglong_le(0x30)
        self.name = self.get_chunk(
            0x38, 72).decode('utf-16').partition(b'\0')[0]


class Gpt(object):
    """Represents GPT partition table.

    Attributes:
        partition_entries (list): List of initialized \
        :class:`GptPartition` objects.
        header (GptHeader): Initialized :class:`GptHeader` object
    """
    def __init__(self):
        self.partition_entries = []

    def load(self, filename, bs=512):
        """Loads GPT partition table.

        Args:
            filename (str): path to file or device to open for reading
            bs (uint): Block size of the volume, default: 512

        Raises:
            IOError: If file does not exist or not readable
        """
        with open(filename, 'rb') as f:
            f.seek(GPT_HEADER_OFFSET + 0x0C)
            header_size = struct.unpack("<I", f.read(4))[0]
            f.seek(GPT_HEADER_OFFSET)

            header_data = f.read(header_size)
            self.header = GptHeader(header_data)

            if (self.header.fields.signature != GPT_SIGNATURE):
                raise Exception("Invalid GPT signature")

            self._load_partition_entries(f, bs)

    def _load_partition_entries(self, fd, bs):
        """Loads the list of :class:`GptPartition` partition entries

        Args:
            bs (uint): Block size of the volume
        """

        fd.seek(self.header.fields.part_lba * bs)
        for p in xrange(0, self.header.fields.num_partitions):
            data = fd.read(self.header.fields.part_size)
            entry = GptPartitionEntry(data)
            if entry.type_guid != uuid.UUID(
                '{00000000-0000-0000-0000-000000000000}'
            ):
                self.partition_entries.append(entry)
            else:
                # stop loading on empty partition entry
                break
