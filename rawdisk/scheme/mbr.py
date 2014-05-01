import struct
import hexdump

MBR_SIGNATURE = 0xAA55
MBR_SIG_SIZE = 2
MBR_SIG_OFFSET = 0x1FE
PT_ENTRY_SIZE = 16
PT_TABLE_OFFSET = 0x1BE
PT_TABLE_SIZE = PT_ENTRY_SIZE * 4
SECTOR_SIZE = 512


class RawStruct:
    def __init__(self):
        self._data = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def load_from_source(self, source, offset, length):
        source.seek(offset)
        self._data = source.read(length)

    def get_chunk(self, offset, length):
        return self.data[offset:offset+length]

    def get_field(self, offset, length, format):
        return struct.unpack(format, self.data[offset:offset+length])[0]

    def get_ubyte(self, offset):
        return struct.unpack("<B", self.data[offset:offset+1])[0]

    def get_ushort(self, offset):
        return struct.unpack("<H", self.data[offset:offset+2])[0]

    def get_uint(self, offset):
        return struct.unpack("<I", self.data[offset:offset+4])[0]

    def hexdump(self):
        hexdump.hexdump(self._data)


class VBR:
    def load(self, raw_data):
        self.raw = raw_data
        self.oem_id = struct.unpack("<8s", raw_data[3:11])[0]

    def hexdump(self):
        hexdump.hexdump(self.raw)


class PartitionEntry(RawStruct):
    def __init__(self):
        RawStruct.__init__(self)

    def load(self, raw_data):
        RawStruct.data.fset(self, raw_data)
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
    def __init__(self):
        RawStruct.__init__(self)
        self.entries = []

    def load(self, raw_data):
        RawStruct.data.fset(self, raw_data)

        for i in range(0, 4):
            entry = PartitionEntry()
            entry.load(self.get_chunk(PT_ENTRY_SIZE * i, PT_ENTRY_SIZE))

            if (entry.part_type != 0):
                self.entries.append(entry)


class MBR(RawStruct):
    def __init__(self):
        RawStruct.__init__(self)
        self.partition_table = PartitionTable()

    def load(self, filename):
        try:
            with open(filename, 'rb') as f:
                # Look for MBR signature first
                self.load_from_source(f, 0, 512)
                signature = self.get_ushort(MBR_SIG_OFFSET)

                if (signature != MBR_SIGNATURE):
                    raise Exception("Invalid MBR signature")

                self.partition_table.load(
                    self.get_chunk(PT_TABLE_OFFSET, PT_TABLE_SIZE)
                )

                for entry in self.partition_table.entries:
                    entry.hexdump()
        except IOError, e:
            print e
