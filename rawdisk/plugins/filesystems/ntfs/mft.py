import hexdump
from mft_entry import *
from rawdisk.util.rawstruct import RawStruct


class MftTable(object):
    def __init__(self, offset):
        self.offset = offset
        self._metadata_entries = []

    def load(self, source):
        self.load_system_entries(source, self.offset)

    def get_system_entry(self, entry_id):
        return self._metadata_entries[entry_id]

    def load_system_entries(self, source, offset):
        source.seek(offset)

        for n in range(0, 12):
        # for n in range(0, 1):
            data = source.read(MFT_ENTRY_SIZE)
            entry = MftEntry(offset, data)
            self._metadata_entries.insert(entry.header.seq_number, entry)
            source.seek(entry.end_offset)
            offset = entry.end_offset