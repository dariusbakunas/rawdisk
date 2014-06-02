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

from rawdisk.filesystems.volume import Volume
from rawdisk.util.rawstruct import RawStruct

VOLUME_HEADER_OFFSET = 1024


class VolumeHeader(RawStruct):
    """Represents HFS+ volume header

    Attributes:
        signature (2 byte string): The volume signature, \
        which must be kHFSPlusSigWord ('H+') for an HFS Plus volume.
        version (ushort): The version of the volume format, \
        which is currently 4 (kHFSPlusVersion) for HFS Plus volumes.
        attributes (uint): HFS+ volume attributes
    """
    def __init__(self, data):
        RawStruct.__init__(self, data)
        self.signature = self.get_string(0x00, 2)
        # HFS+ everything is stored in big-endian
        self.version = self.get_ushort(0x02, True)
        self.attributes = self.get_uint(0x04, True)


class HfsPlusVolume(Volume):
    """Structure for HFS+ volume.

    Attributes:
        fd (fd): file descriptor used to read volume information
        vol_header (VolumeHeader): Initialized :class:`VolumeHeader` object

    See Also:
        https://developer.apple.com/legacy/library/technotes/tn/tn1150.html
    """
    def __init__(self):
        self.fd = None
        self.vol_header = None

    def load(self, filename, offset):
        """Loads HFS+ volume information"""
        try:
            self.offset = offset
            self.fd = open(filename, 'rb')
            # 1024 - temporary, need to find out actual volume header size
            self.fd.seek(self.offset + VOLUME_HEADER_OFFSET)
            data = self.fd.read(1024)
            self.vol_header = VolumeHeader(data)

            self.fd.close()
        except IOError, e:
            print e

    def __str__(self):
        return "Type: HFS+, Offset: 0x%X" % (
            self.offset
        )