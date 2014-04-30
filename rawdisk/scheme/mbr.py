import struct
import hexdump


class MBR:
    def __init__(self):
        self.raw = None

    def load(self, raw_data):
        signature = struct.unpack("<H", raw_data[510:512])[0]

        if (signature != 0xAA55):
            return False

        self.raw = raw_data

        return True

    def hexdump(self):
        hexdump.hexdump(self.raw)