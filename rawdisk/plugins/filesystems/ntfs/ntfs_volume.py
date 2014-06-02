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

import hurry.filesize
from mft import MftTable
from bootsector import BootSector
from rawdisk.filesystems.volume import Volume

NTFS_BOOTSECTOR_SIZE = 512


class NtfsVolume(Volume):
    """Represents NTFS volume.

    Attributes:
        offset (uint): offset to the partition from the start of the disk \
        in bytes
        fd (fd): file descriptor that is used to load volume information
        bootsector (BootSector): initialized :class:`BootSector \
        <plugins.filesystems.ntfs.bootsector.BootSector>` object
        mft_table (MftTable): initialized :class:`MftTable \
        <plugins.filesystems.ntfs.mft.MftTable>` object

    See More:
        http://en.wikipedia.org/wiki/NTFS
    """
    def __init__(self):
        self.offset = 0
        self.bootsector = None
        self.mft_table = None
        self.fd = None

    def load(self, filename, offset):
        """Loads NTFS volume information

        Args:
            filename (str): Path to file/device to read the volume \
            information from.
            offset (uint): Valid NTFS partition offset from the beginning \
            of the file/device.

        Raises:
            IOError: If source file/device does not exist or is not readable
        """
        self.offset = offset
        self.fd = open(filename, 'rb')
        self._load_bootsector()
        self._load_mft_table()
        self.fd.close()

    def _load_bootsector(self):
        self.fd.seek(self.offset)
        data = self.fd.read(NTFS_BOOTSECTOR_SIZE)
        self.bootsector = BootSector(data)

    def _load_mft_table(self):
        self.mft_table = MftTable(self.mft_table_offset)
        self.mft_table.load(self.fd)

    def __str__(self):
        return "Type: NTFS, Offset: 0x%X, Size: %s, MFT Table Offset: 0x%X" % (
            self.offset,
            hurry.filesize.size(self.size),
            self.mft_table_offset
        )

    @property
    def size(self):
        """
        Returns:
            int: Total size of NTFS volume in bytes
        """
        return self.bootsector.bpb.bytes_per_sector * \
            self.bootsector.bpb.total_sectors

    @property
    def mft_table_offset(self):
        """
        Returns:
            int: MFT Table offset from the beginning of the disk in bytes
        """
        return self.offset + self.bootsector.mft_offset
