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

MFT_ENTRY_HEADER_SIZE = 48


class MftEntry(RawStruct):
    """Represents MFT table entry.

    Attributes:
        offset (uint): MFT entry offset starting from the beginning of \
        disk in bytes.
        attributes (list): List of initialized mft attribute objects \
        (eg. :class:`~.mft_attribute.MftAttrStandardInformation`).
        header (MftEntryHeader): Initialized \
        :class:`~.mft_entry_header.MftEntryHeader`.
    """
    def __init__(self, data=None, offset=None, length=None, filename=None):
        RawStruct.__init__(
            self,
            data=data,
            filename=filename,
            offset=offset,
            length=length
        )

        self.attributes = []
        self.fname_str = ""
        header_data = self.get_chunk(0, MFT_ENTRY_HEADER_SIZE)
        self.header = MftEntryHeader(header_data)
        self.name_str = self._get_entry_name(self.header.seq_number)
        self.load_attributes()

    @property
    def used_size(self):
        return self.header.used_size

    def load_attributes(self):
        free_space = self.size - MFT_ENTRY_HEADER_SIZE
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
            (eg. :class:`~.mft_attribute.MftAttrFilename`).
            None: If atttribute type does not mach any one of the supported \
            attribute types.
        """
        attr_type = self.get_uint_le(offset)
        # Attribute length is in header @ offset 0x4
        length = self.get_uint_le(offset + 0x04)
        data = self.get_chunk(offset, length)

        return MftAttr.factory(attr_type, data)

    def _get_entry_name(self, index):
        names = {
            0: "Master File Table",
            1: "Master File Table Mirror",
            2: "Log File",
            3: "Volume File",
            4: "Attribute Definition Table",
            5: "Root Directory",
            6: "Volume Bitmap",
            7: "Boot Sector",
            8: "Bad Cluster List",
            9: "Security",
            10: "Upcase Table",
            11: "Extend Table",
        }

        return names.get(index, "(unknown/unnamed)")

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