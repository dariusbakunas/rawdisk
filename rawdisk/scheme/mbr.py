import struct
import hexdump

MBR_SIGNATURE = 0xAA55
MBR_SIG_SIZE = 2
MBR_SIG_OFFSET = 0x1FE
PT_ENTRY_SIZE = 16
PT_TABLE_OFFSET = 0x1BE
PT_TABLE_SIZE = PT_ENTRY_SIZE * 4


class PartitionEntry:
    def load(self, raw_data):
        self.boot_indicator = struct.unpack("<B", raw_data[:1])[0]


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