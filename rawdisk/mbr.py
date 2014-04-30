import struct


class MBR:
    def __init__(self):
        pass

    def load(self, raw_data):
        signature = struct.unpack("<H", raw_data[510:512])[0]

        if (signature != 0xAA55):
            return False

        return True