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

from mft_attribute import MFT_ATTR_FILENAME, MftAttr
from mft_entry_header import MftEntryHeader
from rawdisk.util.rawstruct import RawStruct

MFT_ENTRY_SIZE = 1024
MFT_ENTRY_HEADER_SIZE = 48

# NTFS System files
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


class MftEntry(RawStruct):
    """Represents MFT table entry.

    Attributes:
        offset (uint): MFT entry offset starting from the beginning of \
        disk in bytes.
        attributes (list): List of initialized mft attribute objects \
        (eg. :class:`MftAttrStandardInformation \
        <plugins.filesystems.ntfs.mft_attribute.MftAttrStandardInformation>`).
        header (MftEntryHeader): Initialized :class:`MftEntryHeader \
        <plugins.filesystems.ntfs.mft_entry_header.MftEntryHeader>`.
    """
    def __init__(self, offset, data):
        RawStruct.__init__(self, data)
        self.offset = offset
        self.attributes = []
        self.name_str = ""
        self.fname_str = ""

        header_data = self.get_chunk(0, MFT_ENTRY_HEADER_SIZE)
        self.header = MftEntryHeader(header_data)
        self.load_attributes()

    @property
    def end_offset(self):
        """
        Returns:
            uint: end offset of the MFT entry, beginning form the start \
            of the disk in bytes."""
        return self.offset + self.header.allocated_size

    @property
    def used_size(self):
        return self.header.used_size

    @property
    def size(self):
        return self.header.allocated_size

    def load_attributes(self):
        free_space = MFT_ENTRY_SIZE - MFT_ENTRY_HEADER_SIZE
        offset = self.header.first_attr_offset

        while free_space > 0:
            attr = self.get_attribute(offset)

            if (attr is not None):
                if attr.header.type == MFT_ATTR_FILENAME:
                    self.fname_str = attr.fname

                self.attributes.append(attr)
                free_space = free_space - attr.header.length
                offset = offset + attr.header.length
            else:
                break

    def get_attribute(self, offset):
        """Determines attribute type at the offset and returns \
        initialized attribute object.

        Returns:
            MftAttr: One of the attribute objects \
            (eg. :class:`MftAttrFilename \
                <plugins.filesystems.ntfs.mft_attribute.MftAttrFilename>`).
            None: If atttribute type does not mach any one of the supported \
            attribute types.
        """
        attr_type = self.get_uint(offset)
        # Attribute length is in header @ offset 0x4
        length = self.get_uint(offset + 0x04)
        data = self.get_chunk(offset, length)

        return MftAttr.factory(attr_type, data)

    def __str__(self):
        result = (
            "File: %d\n%s (%s)" % (
                self.header.seq_number,
                self.name_str,
                self.fname_str
            ))

        for attr in self.attributes:
            result = result + "\n\t" + str(attr)

        return result