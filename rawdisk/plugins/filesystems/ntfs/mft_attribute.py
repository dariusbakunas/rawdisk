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
        header (MftAttrHeader): Initialized :class:`MftAttrHeader \
        <plugins.filesystems.ntfs.mft_attr_header.MftAttrHeader>` object.
    """
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
