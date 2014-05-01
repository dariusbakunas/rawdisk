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

    def hexdump(self):
        hexdump.hexdump(self._data)


class VBR:
    def load(self, raw_data):
        self.raw = raw_data
        self.oem_id = struct.unpack("<8s", raw_data[3:11])[0]

    def hexdump(self):
        hexdump.hexdump(self.raw)


class PartitionEntry:
    def __init__(self):
        self.vbr = VBR()

    def load(self, raw_data):
        self.raw = raw_data
        self.boot_indicator = struct.unpack("<B", raw_data[:1])[0]
        self.starting_head = struct.unpack("<B", raw_data[1:2])[0]
        tmp = struct.unpack("<B", raw_data[2:3])[0]
        self.starting_sector = tmp & 0x3F   # Only bits 0-5 are used
        self.starting_cylinder = ((tmp & 0xC0) << 2) + \
            struct.unpack("<B", raw_data[3:4])[0]
        self.part_type = struct.unpack("<B", raw_data[4:5])[0]
        self.ending_head = struct.unpack("<B", raw_data[5:6])[0]
        tmp = struct.unpack("<B", raw_data[6:7])[0]
        self.ending_sector = tmp & 0x3F
        self.ending_cylinder = ((tmp & 0xC0) << 2) + \
            struct.unpack("<B", raw_data[7:8])[0]
        self.relative_sector = struct.unpack("<I", raw_data[8:12])[0]
        self.total_sectors = struct.unpack("<I", raw_data[12:16])[0]
        self.part_offset = SECTOR_SIZE*self.relative_sector

    def hexdump(self):
        hexdump.hexdump(self.raw)


class PartitionTable:
    def __init__(self):
        self.entries = []

    def load(self, raw_data):
        self.raw = raw_data

        for i in range(0, 4):
            start = PT_ENTRY_SIZE * i
            end = start + PT_ENTRY_SIZE
            entry = PartitionEntry()
            entry.load(self.raw[start:end])

            if (entry.part_type != 0):
                self.entries.append(entry)

    def hexdump(self):
        hexdump.hexdump(self.raw)


class MBR(RawStruct):
    def __init__(self):
        RawStruct.__init__(self)
        self.partition_table = PartitionTable()

    def load(self, filename):
        try:
            with open(filename, 'rb') as f:
                # Look for MBR signature first
                self.load_from_source(f, 0, 512)
                signature = self.get_field(MBR_SIG_OFFSET, MBR_SIG_SIZE, "<H")

                if (signature != MBR_SIGNATURE):
                    raise Exception("Invalid MBR signature")

                self.partition_table.load(
                    self.get_chunk(PT_TABLE_OFFSET, PT_TABLE_SIZE)
                )

                # for entry in self.partition_table.entries:
                #     entry.hexdump()
        except Exception, e:
            print e
