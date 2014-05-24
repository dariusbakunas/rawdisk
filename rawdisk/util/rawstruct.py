import struct
import hexdump


class RawStruct(object):
    def __init__(self, data = None):
        self._data = data

    @property
    def data(self):
        return self._data

    @property
    def size(self):
        return len(self._data)

    @data.setter
    def data(self, value):
        self._data = value

    def load_from_source(self, source, offset, length):
        source.seek(offset)
        self._data = source.read(length)

    def get_chunk(self, offset, length):
        return self.data[offset:offset+length]

    def get_uuid(self, offset):
        (a, b) = struct.unpack(">QQ", self.data[offset:offset+16])
        return (a << 64) | b

    def get_field(self, offset, length, format):
        return struct.unpack(format, self.data[offset:offset+length])[0]

    def get_ubyte(self, offset):
        return struct.unpack("B", self.data[offset:offset+1])[0]

    def get_ushort(self, offset):
        return struct.unpack("<H", self.data[offset:offset+2])[0]

    def get_uint(self, offset):
        return struct.unpack("<I", self.data[offset:offset+4])[0]

    def get_ulong(self, offset):
        return struct.unpack("<L", self.data[offset:offset+4])[0]

    def get_ulonglong(self, offset):
        return struct.unpack("<Q", self.data[offset:offset+8])[0]

    def get_string(self, offset, length):
        return struct.unpack(str(length) + "s", self.data[
            offset:offset+length
        ])[0]

    def hexdump(self):
        hexdump.hexdump(self._data)