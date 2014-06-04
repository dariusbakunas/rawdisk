# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2014 Darius Bakunas

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
                self._data = f.read(length)

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

    def load_from_source(
        self, fd=None, offset=None, length=None
    ):
        """Loads byte array for the structure from the file or device

        Args:
            source (fd): file descriptor used to load data
            offset (int): data offset
            length (int): number of bytes to read
        """

        if offset is None:
            offset = 0

        if (fd is not None):
            fd.seek(offset)
            self._data = fd.read(length)

    def get_chunk(self, offset, length):
        """
        Args:
            offset (int): byte array start [x:]
            length (int): number of bytes to return [:x]
        Returns:
            str: Custom length byte array of the structure.
        """
        return self.data[offset:offset+length]

    def get_uuid(self, offset):
        """Returns Python uuid object initialized with bytes at specified offset

        Args:
            offset (int): offset to 16-byte array
        """
        return uuid.UUID(bytes_le=self.get_string(offset, 16))

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

    def get_uchar(self, offset):
        """Returns unsigned char (1 byte)

        Args:
            offset (int): unsigned char offset in byte array
        """
        return struct.unpack("B", self.data[offset:offset+1])[0]

    def get_ushort(self, offset, big_endian=False):
        """Returns unsigned short (2 bytes)

        Args:
            offset (int): unsigned short offset in byte array
            big_endian (bool): source is big_endian, defaults to little endian
        """
        if (big_endian):
            return struct.unpack(">H", self.data[offset:offset+2])[0]
        return struct.unpack("<H", self.data[offset:offset+2])[0]

    def get_uint(self, offset, big_endian=False):
        """Returns unsigned int (4 bytes)

        Args:
            offset (int): unsigned int offset in byte array
            big_endian (bool): source is big_endian, defaults to little endian
        """
        if (big_endian):
            return struct.unpack(">I", self.data[offset:offset+4])[0]
        return struct.unpack("<I", self.data[offset:offset+4])[0]

    def get_ulong(self, offset, big_endian=False):
        """Returns unsigned long (4 bytes)

        Args:
            offset (int): unsigned long offset in byte array
            big_endian (bool): source is big_endian, defaults to little endian
        """
        if (big_endian):
            return struct.unpack(">L", self.data[offset:offset+4])[0]
        return struct.unpack("<L", self.data[offset:offset+4])[0]

    def get_ulonglong(self, offset, big_endian=False):
        """Returns unsigned long long (8 bytes)

        Args:
            offset (int): unsigned long long offset in byte array
            big_endian (bool): source is big_endian, defaults to little endian
        """
        if (big_endian):
            return struct.unpack(">Q", self.data[offset:offset+8])[0]
        return struct.unpack("<Q", self.data[offset:offset+8])[0]

    def get_string(self, offset, length):
        """Returns string (length bytes)

        Args:
            offset (int): sring offset in byte array
            length (int): string length
        """
        return struct.unpack(str(length) + "s", self.data[
            offset:offset+length
        ])[0]

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