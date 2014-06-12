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


from mft_entry import MftEntry


class MftTable(object):
    """Represents NTFS Master File Table (MFT)

    Args:
        offset (uint): Offset to the MFT table from disk start in bytes.
        mft_record_size (uint): Mft entry size in bytes (default: 1024).
        filename (str): A file to read the data from.

    See More:
        http://en.wikipedia.org/wiki/NTFS#Master_File_Table
    """
    def __init__(
        self,
        mft_entry_size=1024,
        offset=None,
        filename=None
    ):

        if offset is None:
            self.offset = 0
        else:
            self.offset = offset

        self.entry_size = mft_entry_size
        self.filename = filename
        self._entries = {}

    def get_entry(self, entry_id):
        """Get mft entry by index. If entry is not already loaded it will load \
        it from file specified during :class:`MftTable` initialization.

        Returns:
            MftEntry: initialized :class:`~.mft_entry.MftEntry`.
        """

        if entry_id in self._entries:
            return self._entries[entry_id]
        else:
            entry_offset = entry_id * self.entry_size

            # load entry
            entry = MftEntry(
                filename=self.filename,
                offset=self.offset + entry_offset,
                length=self.entry_size
            )

            # cache entry
            self._entries[entry_id] = entry

            return entry

    def preload_entries(self, count):
        """Loads specified number of MFT entries

        Args:
            count (int): Number of entries to preload.

        """
        for n in range(0, count):
            self.get_entry(n)

    def __str__(self):
        result = ""
        for entry_id in self._entries:
            result += str(self._entries[entry_id]) + "\n\n"

        return result