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

import hexdump
from mft_entry import *
from rawdisk.util.rawstruct import RawStruct


class MftTable(object):
    """Represents NTFS Master File Table (MFT)

    Args:
        offset (uint): offset to the MFT table from disk start in bytes

    See More:
        http://en.wikipedia.org/wiki/NTFS#Master_File_Table
    """
    def __init__(self, offset):
        self.offset = offset
        self._metadata_entries = []

    def load(self, source):
        """Loads first 12 mft entries of the table"""
        self._load_system_entries(source, self.offset)

    def get_system_entry(self, entry_id):
        """Get system entry by index

        Returns:
            MftEntry: initialized :class:`MftEntry <plugins.filesystems.ntfs.mft_entry.MftEntry>`
        """
        return self._metadata_entries[entry_id]

    def _load_system_entries(self, source, offset):
        source.seek(offset)

        for n in range(0, 12):
            data = source.read(MFT_ENTRY_SIZE)
            entry = MftEntry(offset, data)
            entry.name_str = self._get_system_entry_name(n)
            self._metadata_entries.append(entry)
            source.seek(entry.end_offset)
            offset = entry.end_offset

    def _get_system_entry_name(self, index):
        if index == 0:
            return "Master File Table"
        elif index == 1:
            return "Master File Table Mirror"
        elif index == 2:
            return "Log File"
        elif index == 3:
            return "Volume File"
        elif index == 4:
            return "Attribute Definition Table"
        elif index == 5:
            return "Root Directory"
        elif index == 6:
            return "Volume Bitmap"
        elif index == 7:
            return "Boot Sector"
        elif index == 8:
            return "Bad Cluster List"
        elif index == 9:
            return "Security"
        elif index == 10:
            return "Upcase Table"
        elif index == 11:
            return "Extend Table"
        else:
            return "(unknown/unnamed)"

    def __str__(self):
        result = ""
        for entry in self._metadata_entries:
            result += str(entry) + "\n\n"

        return result