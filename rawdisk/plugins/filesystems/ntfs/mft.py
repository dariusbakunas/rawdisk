# -*- coding: utf-8 -*-


from .mft_entry import MftEntry

ENTRY_MFT = 0
ENTRY_MFT_MIRROR = 1
ENTRY_LOGFILE = 2
ENTRY_VOLUME = 3
ENTRY_ATTRDEF = 4
ENTRY_ROOT = 5
ENTRY_BITMAP = 6
ENTRY_BOOT = 7
ENTRY_BADCLUS = 8
ENTRY_SECURE = 9
ENTRY_UPCASE = 10
ENTRY_EXTEND = 11


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
                length=self.entry_size,
                index=entry_id
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
