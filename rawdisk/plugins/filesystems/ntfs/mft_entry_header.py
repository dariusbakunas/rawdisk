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


class MftEntryHeader(RawStruct):
    """Represents MFT entry header.

    Attributes:
        file_signature (string): Entry signature (4 bytes) \
        (eg. 'FILE' or 'BAAD').
        update_seq_array_offset (ushort): The offset to the update sequence \
        array, from the start of this structure. The update sequence array \
        must end before the last USHORT value in the first sector.
        update_seq_array_size (ushort): The size of the update sequence \
        array, in bytes.
        logfile_seq_number (ulonglong): ?? (reserved in Microsoft website)
        seq_number (ushort): The sequence number. This value is incremented \
        each time that a file record segment is freed; \
        it is 0 if the segment is not used.
        hard_link_count (ushort): ?? (reserved in Microsoft website)
        first_attr_offset (ushort): The offset of the first attribute \
        record, in bytes.
        flags (ushort): The file flags (FILE_RECORD_SEGMENT_IN_USE (0x0001), \
            FILE_FILE_NAME_INDEX_PRESENT (0x0002)).
        base_file_record (ulonglong): A file reference to the base file \
        record segment for this file. \
        If this is the base file record, the value is 0.

    See Also:
        http://msdn.microsoft.com/en-us/library/bb470124(v=vs.85).aspx
    """
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