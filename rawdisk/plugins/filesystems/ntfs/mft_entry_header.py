from rawdisk.util.rawstruct import RawStruct


class MftEntryHeader(RawStruct):
    def __init__(self, data):
        RawStruct.__init__(self, data)
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