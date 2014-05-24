import uuid
import hexdump
import rawdisk.filesystems
import struct
from rawdisk.util.rawstruct import RawStruct

GPT_HEADER_OFFSET = 0x200
GPT_SIG_SIZE = 8
GPT_SIGNATURE = 'EFI PART'

class GptHeader(RawStruct):
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
    def __init__(self, data):
        RawStruct.__init__(self, data)
        self.type_guid = self.get_uuid(0x00)
        self.part_guid = self.get_uuid(0x10)
        self.first_lba = self.get_ulonglong(0x20)
        self.last_lba = self.get_ulonglong(0x28)
        self.attr_flags = self.get_ulonglong(0x30)
        self.name = self.get_chunk(0x38, 72).decode('utf-16')

class Gpt(object):
    def __init__(self):
        self.partition_entries = []

    def load(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.fd = f
                f.seek(GPT_HEADER_OFFSET + 0x0C)
                header_size = struct.unpack("<I", f.read(4))[0]
                f.seek(GPT_HEADER_OFFSET)
                self.header = GptHeader(f.read(header_size))
                self.load_partition_entries()
        except IOError, e:
            print e

    def load_partition_entries(self, block_size = 512):
        self.fd.seek(self.header.part_lba * block_size)
        for p in xrange(0, self.header.num_partitions):
            data = self.fd.read(self.header.part_size)
            entry = GptPartition(data)
            if entry.type_guid != uuid.UUID('{00000000-0000-0000-0000-000000000000}'):
                self.partition_entries.append(entry)
