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

import os
from mft_entry import MftEntry
from rawdisk.util.rawstruct import RawStruct


class MftTable(RawStruct):
    """Represents NTFS Master File Table (MFT)

    Args:
        offset (uint): Offset to the MFT table from disk start in bytes.
        mft_record_size (uint): Mft entry size in bytes (default: 1024).
        data (str): Byte array to initialize structure with.
        offset (uint): Byte offset from the beginning of file/device or data
        num_entries (uint): Number of mft entries to preload
        filename (str): A file to read the data from.

    See More:
        http://en.wikipedia.org/wiki/NTFS#Master_File_Table
    """
    def __init__(
        self,
        mft_entry_size=1024,
        data=None,
        offset=None,
        num_entries=None,
        filename=None
    ):

        self.entry_size = mft_entry_size

        if offset is None:
            self.offset = 0
        else:
            self.offset = offset

        self.filename = filename

        if (num_entries is not None):
            length = num_entries * self.entry_size
        else:
            if data is not None:
                length = len(data)
                num_entries = length / mft_entry_size
            elif filename is not None:
                length = os.stat(filename).st_size - self.offset
                num_entries = length / mft_entry_size

        RawStruct.__init__(
            self,
            data=data,
            offset=offset,
            length=length,
            filename=filename
        )

        self._entries = []

        # preload entries
        self._preload_entries(num_entries)

    def get_entry(self, entry_id):
        """Get mft entry by index

        Returns:
            MftEntry: initialized :class:`~.mft_entry.MftEntry`.
        """
        if entry_id in self._entries:
            return self._entries[entry_id]
        else:
            entry_offset = entry_id * self.entry_size
            entry = None

            if self.size > entry_offset + self.entry_size:
                data = self.get_chunk(entry_offset, self.entry_size)
                entry = MftEntry(data)
            else:
                # need more data
                with open(self.filename, 'r') as f:
                    f.seek(self.offset + entry_offset)
                    data = f.read(self.entry_size)
                    entry = MftEntry(data)
            # cache entry
            self._entries.insert(
                entry_id,
                entry
            )

            return entry

    def _preload_entries(self, num_entries):
        for n in range(0, num_entries):
            data = self.get_chunk(
                self.entry_size * n, self.entry_size
            )

            entry = MftEntry(data)
            entry.name_str = self._sys_entry_name(n)
            self._entries.append(entry)

    def _sys_entry_name(self, index):
        names = {
            0: "Master File Table",
            1: "Master File Table Mirror",
            2: "Log File",
            3: "Volume File",
            4: "Attribute Definition Table",
            5: "Root Directory",
            6: "Volume Bitmap",
            7: "Boot Sector",
            8: "Bad Cluster List",
            9: "Security",
            10: "Upcase Table",
            11: "Extend Table",
        }

        return names.get(index, "(unknown/unnamed)")

    def __str__(self):
        result = ""
        for entry in self._entries:
            result += str(entry) + "\n\n"

        return result