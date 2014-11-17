# -*- coding: utf-8 -*-


from rawdisk.util.rawstruct import RawStruct
from rawdisk.util.filetimes import filetime_to_dt
from mft_attr_header import MftAttrHeader


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


class MftAttr(RawStruct):
    """Base class for all MFT attributes.

    Attributes:
        type_str (string): String representation of attribute's type eg. \
        $SYSTEM_INFORMATION.
        header (MftAttrHeader): Initialized \
        :class:`~.mft_attr_header.MftAttrHeader` object.
    """
    def __init__(self, data):
        RawStruct.__init__(self, data)
        self.type_str = "$UNKNOWN"
        non_resident_flag = self.get_uchar(8)
        name_length = self.get_uchar(9)
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

    @staticmethod
    def factory(attr_type, data):
        """Returns Initialized attribute object based on attr_type \
        (eg. :class:`MftAttrStandardInformation`)

        Args:
            attr_type (uint): Attribute type number (eg. 0x10 - \
                $STANDARD_INFORMATION)
            data (byte array): Data to initialize attribute object with.
        """

        constructors = {
            MFT_ATTR_STANDARD_INFORMATION: MftAttrStandardInformation,
            MFT_ATTR_ATTRIBUTE_LIST: MftAttrAttributeList,
            MFT_ATTR_FILENAME: MftAttrFilename,
            MFT_ATTR_OBJECT_ID: MftAttrObjectId,
            MFT_ATTR_SECURITY_DESCRIPTOR: MftAttrSecurityDescriptor,
            MFT_ATTR_VOLUME_NAME: MftAttrVolumeName,
            MFT_ATTR_VOLUME_INFO: MftAttrVolumeInfo,
            MFT_ATTR_DATA: MftAttrData,
            MFT_ATTR_INDEX_ROOT: MftAttrIndexRoot,
            MFT_ATTR_INDEX_ALLOCATION: MftAttrIndexAllocation,
            MFT_ATTR_BITMAP: MftAttrBitmap,
            MFT_ATTR_REPARSE_POINT: MftAttrReparsePoint,
            MFT_ATTR_LOGGED_TOOLSTREAM: MftAttrLoggedToolstream,
        }

        if attr_type not in constructors:
            return None

        return constructors[attr_type](data)

    def __str__(self):
        name = "N/A"
        resident = "Resident"

        if hasattr(self.header, 'attr_name'):
            name = self.header.attr_name

        if (self.header.non_resident_flag):
            resident = "Non-Resident"

        return "Type: %s Name: %s %s Size: %d" % (
            self.type_str,
            name,
            resident,
            self.header.length
        )


# Define all attribute types here
class MftAttrStandardInformation(MftAttr):
    """$STANDARD_INFORMATION attribute

    Attributes:
        ctime (ulonglong): File creation date in Microsoft FILETIME format.
        atime (ulonglong): Last file modification date.
        mtime (ulonglong): Last file MFT entry modification date.
        rtime (ulonglong): Last file access date.
        perm (uint): DOS file permissions.
        versions (uint): Maximum number of versions.
        class_id (uint): Class Id.

    Note:
        This attribute is always resident.

    See Also:
        http://ftp.kolibrios.org/users/Asper/docs/NTFS/ntfsdoc.html#attribute_standard_information
    """
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$STANDARD_INFORMATION"
        offset = self.header.size
        # File Creation
        self.ctime = self.get_ulonglong_le(offset)
        # File Alteration
        self.atime = self.get_ulonglong_le(offset + 0x08)
        # MFT Changed
        self.mtime = self.get_ulonglong_le(offset + 0x10)
        # File Read
        self.rtime = self.get_ulonglong_le(offset + 0x18)
        # DOS File Permissions
        self.perm = self.get_uint_le(offset + 0x20)
        # Maximum Number of Versions
        self.versions = self.get_uint_le(offset + 0x20)
        # Version Number
        self.version = self.get_uint_le(offset + 0x28)
        self.class_id = self.get_uint_le(offset + 0x2C)

        # Not all SI headers include 2K fields
        if (self.size > 0x48):
            self.owner_id = self.get_uint_le(offset + 0x30)
            self.sec_id = self.get_uint_le(offset + 0x34)
            self.quata = self.get_ulonglong_le(offset + 0x38)
            self.usn = self.get_ulonglong_le(offset + 0x40)

    @property
    def ctime_dt(self):
        """
        Returns:
            datetime: File creation date in Python's datetime format.
        """
        return filetime_to_dt(self.ctime)

    @property
    def atime_dt(self):
        """
        Returns:
            datetime: File modification date in Python's datetime format.
        """
        return filetime_to_dt(self.atime)

    @property
    def mtime_dt(self):
        """
        Returns:
            datetime: MFT entry modification date in Python's datetime format.
        """
        return filetime_to_dt(self.mtime)

    @property
    def rtime_dt(self):
        """
        Returns:
            datetime: Last file access date in Python's datetime format.
        """
        return filetime_to_dt(self.rtime)


class MftAttrAttributeList(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$ATTRIBUTE_LIST"


class MftAttrFilename(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        self.type_str = "$FILE_NAME"
        # $Filename is always resident
        offset = self.header.size
        self.parent_ref = self.get_ulonglong_le(offset)
        self.ctime = self.get_ulonglong_le(offset + 0x08)
        self.atime = self.get_ulonglong_le(offset + 0x10)
        self.mtime = self.get_ulonglong_le(offset + 0x18)
        self.rtime = self.get_ulonglong_le(offset + 0x20)
        self.alloc_size = self.get_ulonglong_le(offset + 0x28)
        self.real_size = self.get_ulonglong_le(offset + 0x30)
        self.flags = self.get_uint_le(offset + 0x38)
        # Used by EAs and Reparse ??
        self.reparse = self.get_uint_le(offset + 0x3C)
        self.fname_length = self.get_uchar(offset + 0x40)
        self.fnspace = self.get_uchar(offset + 0x41)
        self.fname = self.get_chunk(offset + 0x42, 2 *
                                    self.fname_length).decode('utf-16')

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
        offset = self.header.size
        length = self.header.length - self.header.size
        self.vol_name = self.get_chunk(
            offset, 2 * length).decode('utf-16').partition(b'\0')[0]

# Volume Flags
VOLUME_IS_DIRTY = 0x0001
VOLUME_RESIZE_LOG_FILE = 0x0002
VOLUME_UPGRADE_ON_MOUNT = 0x0004
VOLUME_MOUNTED_ON_NT4 = 0x0008
VOLUME_DELETE_USN_UNDERWAY = 0x0010
VOLUME_REPAIR_OBJECT_ID = 0x0020
VOLUME_MODIFIED_BY_CHDSK = 0x8000


class MftAttrVolumeInfo(MftAttr):
    def __init__(self, data):
        MftAttr.__init__(self, data)
        offset = self.header.size
        self.type_str = "$VOLUME_INFORMATION"
        self.major_ver = self.get_uchar(offset + 0x08)
        self.minor_ver = self.get_uchar(offset + 0x09)
        self.flags = self.get_ushort_le(offset + 0x0A)


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
