import hexdump
from rawdisk.util.rawstruct import RawStruct

MFT_ENTRY_SIZE = 1024


class MFT_Entry_Header(RawStruct):
    def __init__(self):
        pass

    def load(self, data):
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

class MFT_Attribute_Header(RawStruct):
    def __init__(self):
        pass


class MFT_Attribute(RawStruct):
    def __init__(self):
        pass


class MFT_Entry(RawStruct):
    def __init__(self, offset):
        self.offset = offset
        self.header = MFT_Entry_Header()
        self.attributes = []

    def load(self, data):
        RawStruct.data.fset(self, data)
        self.header.load(data)

        # print "Attr offset:", hex(self.header.first_attr_offset)

    @property
    def used_size(self):
        return self.header.used_size

    @property
    def size(self):
        return self.header.allocated_size

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
        self.mft_entries = []

    def load(self, source):
        source.seek(self.offset)
        data = source.read(MFT_ENTRY_SIZE)
        first_mft_entry = MFT_Entry(self.offset)
        first_mft_entry.load(data)
        
        second_mft_offset = first_mft_entry.offset+first_mft_entry.header.allocated_size
        source.seek(second_mft_offset)
        data = source.read(MFT_ENTRY_SIZE)
        # hexdump.hexdump(data)
