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
            data = source.read(MFT_ENTRY_SIZE)
            entry = MftEntry(offset, data)
            entry.name_str = self.get_system_entry_name(n)
            self._metadata_entries.append(entry)
            source.seek(entry.end_offset)
            offset = entry.end_offset

    def get_system_entry_name(self, index):
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