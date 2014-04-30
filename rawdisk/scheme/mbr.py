import struct
import hexdump

MBR_SIGNATURE = 0xAA55
MBR_SIG_SIZE = 2
MBR_SIG_OFFSET = 0x1FE
PT_ENTRY_SIZE = 16
PT_TABLE_OFFSET = 0x1BE
PT_TABLE_SIZE = PT_ENTRY_SIZE * 4
SECTOR_SIZE = 512


class PartitionEntry:
    def load(self, raw_data):
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


class PartitionTable:
    def __init__(self):
        self.entries = []

    def load(self, raw_data):
        self.raw = raw_data[
            PT_TABLE_OFFSET:PT_TABLE_OFFSET + PT_TABLE_SIZE
        ]

        for i in range(0, 4):
            start = PT_ENTRY_SIZE * i
            end = start + PT_ENTRY_SIZE
            entry = PartitionEntry()
            entry.load(self.raw[start:end])
            if (entry.part_type != 0):
                    self.entries.append(entry)

    def hexdump(self):
        hexdump.hexdump(self.raw)


class MBR:
    def __init__(self):
        self.partition_table = PartitionTable()

    def load(self, raw_data):
        signature = struct.unpack("<H", raw_data[
            MBR_SIG_OFFSET:MBR_SIG_OFFSET+MBR_SIG_SIZE
        ])[0]

        if (signature != MBR_SIGNATURE):
            return False

        self.raw = raw_data
        self.partition_table.load(self.raw)

        return True

    def hexdump(self):
        hexdump.hexdump(self.raw)