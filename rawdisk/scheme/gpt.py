import uuid
import hexdump
import rawdisk.filesystems
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
        self.disk_guid = uuid.UUID(int = self.get_uuid(0x38))
        self.part_lba = self.get_ulonglong(0x48)
        self.num_partitions = self.get_uint(0x50)
        self.part_size = self.get_uint(0x54)
        self.part_array_crc32 = self.get_uint(0x58)
        # Rest of bytes @ 0x5C must be zeroes (420 for 512 sectors)


class Gpt(RawStruct):
    def __init__(self):
        RawStruct.__init__(self)
        self.partitions = []

    def load(self, filename):
        try:
            with open(filename, 'rb') as f:
                # TODO: determine size of gpt structure
                self.load_from_source(f, 0, 1024)
                header_size = self.get_uint(GPT_HEADER_OFFSET + 0x0C)
                self.header = GptHeader(self.get_chunk(GPT_HEADER_OFFSET, header_size))
        except IOError, e:
            print e