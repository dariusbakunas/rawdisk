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

from bpb import Bpb
from rawdisk.util.rawstruct import RawStruct

BPB_SIZE = 25
BPB_OFFSET = 0x0B
EXTENDED_BPB_SIZE = 48


class BootSector(RawStruct):
    """Represents NTFS Bootsector

    Attributes:
        oem_id (8 byte string): NTFS filesystem signature 'NTFS    '
        bpb (Bpb): Initialized :class:\
        `Bpb <plugins.filesystems.ntfs.bpb.Bpb>` object
        mft_offset (int): Offset to MFT table from the start of \
        NTFS volume in bytes

    See More:
        http://ntfs.com/ntfs-partition-boot-sector.htm
    """
    def __init__(self, data=None):
        RawStruct.__init__(self, data)
        self.oem_id = self.get_string(3, 8)
        self.bpb = Bpb(self.get_chunk(
            BPB_OFFSET, BPB_SIZE + EXTENDED_BPB_SIZE))
        self.mft_offset = self.bpb.bytes_per_sector * \
            self.bpb.sectors_per_cluster * self.bpb.mft_cluster