import hexdump
from rawdisk.util.rawstruct import RawStruct
from rawdisk.util.filetimes import filetime_to_dt


MFT_ATTR_STANDARD_INFORMATION = 0x10
MFT_ATTR_ATTRIBUTE_LIST = 0x20
MFT_ATTR_FILENAME = 0x30
MFT_ATTR_OBJECT_ID = 0x40
MFT_ATTR_SECURITY_DESCRIPTOR = 0x50
MFT_ATTR_VOLUME_NAME = 0x60
MFT_ATTR_VOLUME_INFO = 0x70
MFT_ATTR_DATA = 0x80
MFT_ATTR_INDEX_ROOT = 0x90
MFT_ATTR_INDEX_ALLOCATION = 0xA0
MFT_ATTR_BITMAP = 0xB0
MFT_ATTR_REPARSE_POINT = 0xC0
MFT_ATTR_LOGGED_TOOLSTREAM = 0x100

# Attribute flags
ATTR_IS_COMPRESSED = 0x0001
ATTR_COMPRESSION_MASK = 0x00ff
ATTR_IS_ENCRYPTED = 0x4000
ATTR_IS_SPARSE = 0x8000


class MftAttrHeader(RawStruct):
    def __init__(self, data):
        RawStruct.__init__(self, data)
        self.type = self.get_uint(0)
        self.length = self.get_uint(0x4)
        self.non_resident_flag = self.get_ubyte(0x08)   # 0 - resident, 1 - not
        self.length_of_name = self.get_ubyte(0x09)      # Used only for ADS
        self.offset_to_name = self.get_ushort(0x0A)     # Used only for ADS
        self.flags = self.get_ushort(0x0C)  # (Compressed, Encrypted, Sparse)
        self.identifier = self.get_ushort(0x0E)

        if (self.non_resident_flag):
            # Attribute is Non-Resident
            self.start_vcn = self.get_ulonglong(0x10)
            self.last_vcn = self.get_ulonglong(0x18)
            self.dr_offset = self.get_ushort(0x20)
            self.comp_unit_size = self.get_ushort(0x22)
            # 4 byte 0x00 padding @ 0x24
            self.alloc_size = self.get_ulonglong(0x28)
            self.real_size = self.get_ulonglong(0x30)
            self.data_size = self.get_ulonglong(0x38)
            if (self.length_of_name > 0):
                self.attr_name = self.get_chunk(0x40, 2 * self.length_of_name).decode('utf-16')
                # print self.attr_name.decode('utf-16')
        else:
            # Attribute is Resident
            self.attr_length = self.get_uint(0x10)
            self.attr_offset = self.get_ushort(0x14)
            self.indexed = self.get_ubyte(0x16)
            if (self.length_of_name > 0):
                self.attr_name = self.get_chunk(0x18, 2 * self.length_of_name).decode('utf-16')
                # print self.attr_name.decode('utf-16')
            # The rest byte is 0x00 padding
            # print "Attr Offset: 0x%x" % (self.attr_offset)


class MftAttr(RawStruct):
    def __init__(self, data):
        RawStruct.__init__(self, data)
        self.type_str = "$UNKNOWN"
        non_resident_flag = self.get_ubyte(8)
        name_length = self.get_ubyte(9)
        header_size = 0

        if non_resident_flag:
            if name_length == 0:
                # Non Resident, No Name
                header_size = 0x40
            else:
                # Non Resident, Has Name
                header_size = 0x40 + 2 * name_length
        else:
            if name_length == 0:
                # Resident, No Name
                header_size = 0x18
            else:
                # Resident, Has Name
                header_size = 0x18 + 2 * name_length

        self.header = MftAttrHeader(
            self.get_chunk(0, header_size)
        )

    def __str__(self):
        if (not self.header.non_resident_flag):
            return "%s (resident)" % (self.type_str)
        else:
            # TODO: Not correct, fix
            return """%s (nonresident):
            logical sectors %d - %d (%x - %x)""" % (
                self.type_str,
                self.header.start_vcn,
                self.header.last_vcn,
                self.header.start_vcn,
                self.header.last_vcn
            )


# Define all attribute types here
class MftAttrStandardInformation(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$STANDARD_INFORMATION"
        if (not self.header.non_resident_flag):
            offset = self.header.size
            # File Creation
            self.ctime = self.get_ulonglong(offset)
            # File Alteration
            self.atime = self.get_ulonglong(offset + 0x08)
            # MFT Changed
            self.mtime = self.get_ulonglong(offset + 0x10)
            # File Read
            self.rtime = self.get_ulonglong(offset + 0x18)
            # DOS File Permissions
            self.perm = self.get_uint(offset + 0x20)
            # Maximum Number of Versions
            self.versions = self.get_uint(offset + 0x20)
            # Version Number
            self.version = self.get_uint(offset + 0x28)
            self.class_id = self.get_uint(offset + 0x2C)

            # Not all SI headers include 2K fields
            if (self.size > 0x48):
                self.owner_id = self.get_uint(offset + 0x30)
                self.sec_id = self.get_uint(offset + 0x34)
                self.quata = self.get_ulonglong(offset + 0x38)
                self.usn = self.get_ulonglong(offset + 0x40)

    @property
    def ctime_dt(self):
        return filetime_to_dt(self.ctime)

    @property
    def atime_dt(self):
        return filetime_to_dt(self.atime)

    @property
    def mtime_dt(self):
        return filetime_to_dt(self.mtime)

    @property
    def rtime_dt(self):
        return filetime_to_dt(self.rtime)


class MftAttrAttributeList(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$ATTRIBUTE_LIST"


class MftAttrFilename(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$FILE_NAME"
        if (not self.header.non_resident_flag):
            offset = self.header.size
            self.parent_ref = self.get_ulonglong(offset)
            self.ctime = self.get_ulonglong(offset + 0x08)
            self.atime = self.get_ulonglong(offset + 0x10)
            self.mtime = self.get_ulonglong(offset + 0x18)
            self.rtime = self.get_ulonglong(offset + 0x20)
            self.alloc_size = self.get_ulonglong(offset + 0x28)
            self.real_size = self.get_ulonglong(offset + 0x30)
            self.flags = self.get_uint(offset + 0x38)
            # Used by EAs and Reparse ??
            self.reparse = self.get_uint(offset + 0x3C)
            self.fname_length = self.get_ubyte(offset + 0x40)
            self.fnspace = self.get_ubyte(offset + 0x41)
            self.fname = self.get_chunk(offset + 0x42, 2 * self.fname_length)

    @property
    def ctime_dt(self):
        return filetime_to_dt(self.ctime)

    @property
    def atime_dt(self):
        return filetime_to_dt(self.atime)

    @property
    def mtime_dt(self):
        return filetime_to_dt(self.mtime)

    @property
    def rtime_dt(self):
        return filetime_to_dt(self.rtime)


class MftAttrObjectId(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$OBJECT_ID"


class MftAttrSecurityDescriptor(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$SECURITY_DESCRIPTOR"


class MftAttrVolumeName(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$VOLUME_NAME"


class MftAttrVolumeInfo(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$VOLUME_INFORMATION"


class MftAttrData(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$DATA"


class MftAttrIndexRoot(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$INDEX_ROOT"


class MftAttrIndexAllocation(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$INDEX_ALLOCATION"


class MftAttrBitmap(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$BITMAP"


class MftAttrReparsePoint(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$REPARSE_POINT"


class MftAttrLoggedToolstream(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$LOGGED_UTILITY_STREAM"
