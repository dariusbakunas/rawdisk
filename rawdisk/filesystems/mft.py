import hexdump
from mft_attribute import *
from rawdisk.util.rawstruct import RawStruct

MFT_ENTRY_SIZE = 1024
MFT_ENTRY_HEADER_SIZE = 48


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
    def __init__(self, offset):
        self.offset = offset
        self.attributes = []

    def load(self, data):
        RawStruct.data.fset(self, data)

        header_data = self.get_chunk(0, MFT_ENTRY_HEADER_SIZE)
        self.header = MFT_Entry_Header(header_data)
        self.header.hexdump()

        first_attribute = self.get_attribute(self.header.first_attr_offset)


    @property
    def used_size(self):
        return self.header.used_size

    @property
    def size(self):
        return self.header.allocated_size


    def get_attribute(self, offset):
        attr_type = self.get_uint(offset)
        length = self.get_uint(offset + 4)  # Attribute length is in header @ offset 0x4
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

        # Metadata MFT entries
        # The Master File Table
        self.mft = None
        # The Master File Table Mirror
        self.mft_mirror = None
        # A log file containing a list of transactions 
        self.log_file = None
        # Information about the colume
        self.volume = None
        # Defines attributes
        self.attr_def = None
        # Root folder
        self.root = None
        # Cluster bitmap representing the volume
        self.bitmap = None
        # Boot sector
        self.boot = None
        # Contains bad clusters for a volume
        self.bad_clust = None
        # Contains security descriptors for all files
        # within the volume
        self.secure = None
        # Converts lowercase characters to 
        # Unicode uppercase characters
        self.upcase = None
        # Used for various option extensions
        self.extend = None


    def load(self, source):
        source.seek(self.offset)
        data = source.read(MFT_ENTRY_SIZE)
        first_mft_entry = MFT_Entry(self.offset)
        first_mft_entry.load(data)
        
        second_mft_offset = first_mft_entry.offset+first_mft_entry.header.allocated_size
        source.seek(second_mft_offset)
        data = source.read(MFT_ENTRY_SIZE)
        # hexdump.hexdump(data)
