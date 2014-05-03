import hexdump
from mft_attribute import *
from rawdisk.util.rawstruct import RawStruct

MFT_ENTRY_SIZE = 1024
MFT_ENTRY_HEADER_SIZE = 48

MFT_ENTRY_MFT = 0x0
MFT_ENTRY_MFTMIRROR = 0x1
MFT_ENTRY_LOGFILE = 0x2
MFT_ENTRY_VOLUME = 0x3
MFT_ENTRY_ATTRDEF = 0x4
MFT_ENTRY_ROOT = 0x5
MFT_ENTRY_BITMAP = 0x6
MFT_ENTRY_BOOT = 0x7
MFT_ENTRY_BADCLUS = 0x8
MFT_ENTRY_SECURE = 0x9
MFT_ENTRY_UPCASE = 0xA
MFT_ENTRY_EXTEND = 0xB


class MFT_Entry_Header(RawStruct):
    def __init__(self, data):
        RawStruct.data.fset(self, data)
        self.file_signature = self.get_string(0, 4)
        self.update_seq_array_offset = self.get_ushort(4)
        self.update_seq_array_size = self.get_ushort(6)
        self.logfile_seq_number = self.get_ulonglong(8)
        self.seq_number = self.get_ushort(16)
        self.hard_link_count = self.get_ushort(18)
        self.first_attr_offset = self.get_ushort(20)
        self.flags = self.get_ushort(22)
        self.used_size = self.get_uint(24)
        self.allocated_size = self.get_ushort(28)
        self.base_file_record = self.get_ulonglong(30)
        self.next_attr_id = self.get_ushort(38)
        self.mft_record_number = self.get_uint(42)


class MFT_Entry(RawStruct):
    def __init__(self, offset, data):
        RawStruct.data.fset(self, data)
        self.offset = offset
        self.attributes = []
        header_data = self.get_chunk(0, MFT_ENTRY_HEADER_SIZE)
        self.header = MFT_Entry_Header(header_data)
        # first_attribute = self.get_attribute(self.header.first_attr_offset)

    @property
    def end_offset(self):
        return self.offset + self.header.allocated_size

    @property
    def used_size(self):
        return self.header.used_size

    @property
    def size(self):
        return self.header.allocated_size

    def get_attribute(self, offset):
        attr_type = self.get_uint(offset)
        # Attribute length is in header @ offset 0x4
        length = self.get_uint(offset + 4)
        data = self.get_chunk(offset, length)
        return MFT_Attribute(data)

    def __str__(self):
        return "MFT Record no: %d, " \
            "Offset: 0x%x, " \
            "Size: %d, " \
            "Used Size: %d, " \
            "Signature: %s" % (
                self.header.mft_record_number,
                self.offset,
                self.size,
                self.used_size,
                self.header.file_signature
            )


class MFT_Table:
    def __init__(self, offset):
        self.offset = offset
        self._metadata_entries = []

    def load(self, source):
        self.load_metadata_entries(source, self.offset)
        entry = self.get_metadata_entry(MFT_ENTRY_ROOT)
        entry.hexdump()

    def get_metadata_entry(self, entry_id):
        return self._metadata_entries[entry_id]

    def load_metadata_entries(self, source, offset):
        source.seek(offset)

        for n in range(0, 12):
            data = source.read(MFT_ENTRY_SIZE)
            entry = MFT_Entry(offset, data)
            self._metadata_entries.append(entry)
            source.seek(entry.end_offset)
            offset = entry.end_offset
