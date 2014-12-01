# -*- coding: utf-8 -*-

import struct
import hexdump
import uuid


class RawStruct(object):
    """Helper class used as a parent class for most filesystem structures.

    Args:
        data (str): Byte array to initialize structure with.
        filename (str): A file to read the data from.
        offset (int): Offset into data or file (if specified).
        length (int): Number of bytes to read.
    """
    def __init__(self, data=None, offset=None, length=None, filename=None):
        if offset is None:
            offset = 0

        if data is not None:
            if length is None:
                self._data = data[offset:]
            else:
                self._data = data[offset:offset+length]
        elif filename is not None:
            with open(filename, 'rb') as f:
                f.seek(offset)
                if length is None:
                    self._data = f.read()
                else:
                    self._data = f.read(length)
        else:
            raise ValueError("Data or filename must be specified.")

    @property
    def data(self):
        """
        Returns:
            str: Byte array of the structure.
        """
        return self._data

    @property
    def size(self):
        """
        Returns:
            int: Size of structure's byte array.
        """
        return len(self._data)

    def get_chunk(self, offset, length):
        """
        Args:
            offset (int): byte array start [x:]
            length (int): number of bytes to return [:x]
        Returns:
            str: Custom length byte array of the structure.
        """
        return self.data[offset:offset+length]

    def get_uuid_le(self, offset):
        """Returns Python uuid object initialized with bytes at specified offset

        Args:
            offset (int): offset to 16-byte little-endian array
        """
        return uuid.UUID(bytes_le=self.get_string(offset, 16))

    def get_uuid_be(self, offset):
        """Returns Python uuid object initialized with bytes at specified offset

        Args:
            offset (int): offset to 16-byte big-endian array
        """
        return uuid.UUID(bytes=self.get_string(offset, 16))

    def get_field(self, offset, length, format):
        """Returns unpacked Python struct array.

        Args:
            offset (int): offset to byte array within structure
            length (int): how many bytes to unpack
            format (str): Python struct format string for unpacking

        See Also:
            https://docs.python.org/2/library/struct.html#format-characters
        """
        return struct.unpack(format, self.data[offset:offset+length])[0]

    def get_ubyte(self, offset):
        """Returns unsigned char (1 byte)

        Args:
            offset (uchar): unsigned char offset in byte array
        """
        return struct.unpack("B", self.data[offset:offset+1])[0]

    def get_byte(self, offset):
        """Returns char (1 byte)

        Args:
            offset (char): signed char offset in byte array
        """
        return struct.unpack("b", self.data[offset:offset+1])[0]

    def get_ushort_le(self, offset):
        """Returns unsigned short (2 bytes),
        assuming source is little-endian.

        Args:
            offset (int): unsigned short offset in byte array.
        """
        return struct.unpack("<H", self.data[offset:offset+2])[0]

    def get_ushort_be(self, offset):
        """Returns unsigned short (2 bytes),
        assuming source is big-endian.

        Args:
            offset (int): unsigned short offset in byte array.
        """
        return struct.unpack(">H", self.data[offset:offset+2])[0]

    def get_uint_le(self, offset):
        """Returns unsigned int (4 bytes)

        Args:
            offset (int): unsigned int offset in little-endian byte array
        """
        return struct.unpack("<I", self.data[offset:offset+4])[0]

    def get_uint_be(self, offset):
        """Returns unsigned int (4 bytes)

        Args:
            offset (int): unsigned int offset in big-endian byte array
        """
        return struct.unpack(">I", self.data[offset:offset+4])[0]

    def get_int_le(self, offset):
        """Returns int (4 bytes)

        Args:
            offset (int): int offset in little-endian byte array
        """
        return struct.unpack("<I", self.data[offset:offset+4])[0]

    def get_ulong_le(self, offset):
        """Returns unsigned long (4 bytes)

        Args:
            offset (int): unsigned long offset in little-endian byte array
        """
        return struct.unpack("<L", self.data[offset:offset+4])[0]

    def get_ulong_be(self, offset):
        """Returns unsigned long (4 bytes)

        Args:
            offset (int): unsigned long offset in big-endian byte array
        """
        return struct.unpack(">L", self.data[offset:offset+4])[0]

    def get_ulonglong_le(self, offset):
        """Returns unsigned long long (8 bytes)

        Args:
            offset (int): unsigned long long offset in little-endian byte array
        """
        return struct.unpack("<Q", self.data[offset:offset+8])[0]

    def get_ulonglong_be(self, offset):
        """Returns unsigned long long (8 bytes)

        Args:
            offset (int): unsigned long long offset in big-endian byte array
        """
        return struct.unpack(">Q", self.data[offset:offset+8])[0]

    def get_string(self, offset, length):
        """Returns string (length bytes)

        Args:
            offset (int): sring offset in byte array
            length (int): string length
        """
        return struct.unpack(str(length) + "s", self.data[
            offset:offset+length
        ])[0]

    def export(self, filename, offset=0, length=None):
        """Exports byte array to specified destination

        Args:
            filename (str): destination to output file
        """
        with open(filename, 'w') as f:
            output = self.data

            if (length is None):
                length = len(self.data) - offset

            if (offset > 0):
                output = self.data[offset:length]
            else:
                output = self.data[:length]

            f.write(output)

    def hexdump(self):
        """Prints structure's data in hex format.

        >>> 00000000: 46 49 4C 45 30 00 03 00  EA 22 20 00 00 00 00 00  \
        FILE0...." .....
        >>> 00000010: 01 00 01 00 38 00 01 00  A0 01 00 00 00 04 00 00  \
        ....8...........
        >>> 00000020: 00 00 00 00 00 00 00 00  06 00 00 00 00 00 00 00  \
        ................

        See More:
            https://bitbucket.org/techtonik/hexdump/
        """
        hexdump.hexdump(self._data)
