# -*- coding: utf-8 -*-


import uuid
import struct
from rawdisk.util.rawstruct import RawStruct
from .headers import GPT_HEADER, GPT_PARTITION_ENTRY
from ctypes import c_ubyte


GPT_HEADER_OFFSET = 0x200
GPT_SIG_SIZE = 8
GPT_SIGNATURE = b'EFI PART'


class GptPartitionEntry(RawStruct):
    def __init__(self, data):
        RawStruct.__init__(self, data)

        self.fields = GPT_PARTITION_ENTRY(
            (c_ubyte * 16).from_buffer_copy(
                self.get_chunk(0, 16)),                 # type_guid
            (c_ubyte * 16).from_buffer_copy(
                self.get_chunk(0x10, 16)),              # part_guid
            self.get_ulonglong_le(0x20),                # first_lba
            self.get_ulonglong_le(0x28),                # last_lba
            self.get_ulonglong_le(0x30),                # attr_flags
            self.get_chunk(0x38, 72).decode('utf-16'),  # name
        )

    @property
    def type_guid(self):
        return uuid.UUID(bytes_le=bytes(self.fields.type_guid))

    @property
    def part_guid(self):
        return uuid.UUID(bytes_le=bytes(self.fields.part_guid))


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
            self.header = GPT_HEADER(header_data)

            if (self.header.signature != GPT_SIGNATURE):
                raise Exception("Invalid GPT signature")

            self._load_partition_entries(f, bs)

    def _load_partition_entries(self, fd, bs):
        """Loads the list of :class:`GptPartition` partition entries

        Args:
            bs (uint): Block size of the volume
        """

        fd.seek(self.header.part_lba * bs)
        for p in range(0, self.header.num_partitions):
            data = fd.read(self.header.part_size)
            entry = GptPartitionEntry(data)
            if entry.type_guid != uuid.UUID(
                '{00000000-0000-0000-0000-000000000000}'
            ):
                self.partition_entries.append(entry)
            else:
                # stop loading on empty partition entry
                break
