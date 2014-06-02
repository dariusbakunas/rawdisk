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


class MftAttrHeader(RawStruct):
    """Represents MFT attribute header.

    Attributes:
        type (uint): Attribute type.
        length (uint): Attribute length (including this header).
        non_resident_flag (ubyte): Non-resident flag (0 - resident, \
            1 - otherwise).
        length_of_name (ubyte): If attribute has name, this is name \
        length in bytes.
        offset_to_name (ushort): Offset to attribute's name in bytes.
        attr_name (unicode): Attribuet's name (if it has one).
        flags (ushort): The attribute flags (COMPRESSION_MASK (0x00FF), \
            SPARSE (0x8000), ENCRYPTED (0x4000)).
        identifier (ushort): The unique identifier for this attribute \
        in the file record.

        Resident attribute:
        attr_length (uint): The size of the attribute value, in bytes.
        attr_offset (ushort): The offset to the value from the start of \
        the attribute record, in bytes.
        indexed (ubyte): Indexed flag??

        Non-resident attribute:
        lowest_vcn (ulonglong): The lowest virtual cluster number (VCN) \
        covered by this attribute record.
        highest_vcn (ulonglong): The highest VCN covered by this \
        attribute record.
        mapping_pairs_offset (ushort): The offset to the mapping \
        pairs array from the start of the attribute record, in bytes.
        comp_unit_size (ushort): Compression unit size = 2 x clusters. \
        0 implies uncompressed.
        alloc_size (ulonglong): The allocated size of the file, in bytes. \
        This value is an even multiple of the cluster size. \
        This member is not valid if the LowestVcn member is nonzero.
        real_size (ulonglong): The file size (highest byte that can be \
            read plus 1), in bytes. \
        This member is not valid if LowestVcn is nonzero.
        data_size (ulonglong): The valid data length (highest initialized \
            byte plus 1), in bytes. This value is rounded to the nearest \
        cluster boundary. This member is not valid if LowestVcn is nonzero.


    See More:
        | http://ftp.kolibrios.org\
/users/Asper/docs/NTFS/ntfsdoc.html#concept_attribute_header
        | http://msdn.microsoft.com/en-us/library/bb470039(v=vs.85).aspx
    """
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
            self.lowest_vcn = self.get_ulonglong(0x10)
            self.highest_vcn = self.get_ulonglong(0x18)
            self.mapping_pairs_offset = self.get_ushort(0x20)
            self.comp_unit_size = self.get_ushort(0x22)
            # 4 byte 0x00 padding @ 0x24
            self.alloc_size = self.get_ulonglong(0x28)
            self.real_size = self.get_ulonglong(0x30)
            self.data_size = self.get_ulonglong(0x38)

            if (self.length_of_name > 0):
                self.attr_name = self.get_chunk(
                    0x40, 2 * self.length_of_name).decode('utf-16')
                # print self.attr_name.decode('utf-16')
        else:
            # Attribute is Resident
            self.attr_length = self.get_uint(0x10)
            self.attr_offset = self.get_ushort(0x14)
            self.indexed = self.get_ubyte(0x16)
            if (self.length_of_name > 0):
                self.attr_name = self.get_chunk(
                    0x18, 2 * self.length_of_name).decode('utf-16')
                # print self.attr_name.decode('utf-16')
            # The rest byte is 0x00 padding
            # print "Attr Offset: 0x%x" % (self.attr_offset)
            