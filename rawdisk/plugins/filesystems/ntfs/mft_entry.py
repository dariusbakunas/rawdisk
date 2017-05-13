# -*- coding: utf-8 -*-


from .mft_attribute import MFT_ATTR_FILENAME, MftAttr
from rawdisk.util.rawstruct import RawStruct
from .headers import MFT_RECORD_HEADER

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
    def __init__(
        self, data=None, offset=None, length=None,
        filename=None, index=None
    ):
        RawStruct.__init__(
            self,
            data=data,
            filename=filename,
            offset=offset,
            length=length
        )

        self.index = index
        self.attributes = []
        self.fname_str = ""

        self.header = MFT_RECORD_HEADER(
            self.get_string(0, 4),      # signature
            self.get_ushort_le(4),      # upd_seq_array_offset
            self.get_ushort_le(6),      # upd_seq_array_size
            self.get_ulonglong_le(8),   # logfile_seq_number
            self.get_ushort_le(16),     # seq_number
            self.get_ushort_le(18),     # hard_link_count
            self.get_ushort_le(20),     # first_attr_offset
            self.get_ushort_le(22),     # flags
            self.get_uint_le(24),       # used_size
            self.get_ushort_le(28),     # allocated_size
            self.get_ulonglong_le(30),  # base_file_record
            self.get_ushort_le(38),     # next_attr_id
            self.get_uint_le(42)        # mft_record_number
        )

        self.name_str = self._get_entry_name(self.index)
        self._load_attributes()

    @property
    def is_directory(self):
        return self.header.flags & 0x0002

    @property
    def is_file(self):
        return not self.is_directory

    @property
    def is_in_use(self):
        return self.header.flags & 0x0001

    @property
    def used_size(self):
        return self.header.used_size

    def _load_attributes(self):
        free_space = self.size - MFT_ENTRY_HEADER_SIZE
        offset = self.header.first_attr_offset

        while free_space > 0:
            attr = self._get_attribute(offset)

            if (attr is not None):
                if attr.header.type == MFT_ATTR_FILENAME:
                    self.fname_str = attr.fname

                self.attributes.append(attr)
                free_space = free_space - attr.header.length
                offset = offset + attr.header.length
            else:
                break

    def lookup_attribute(self, attr_type_id):
        for attr in self.attributes:
            if attr.header.type == attr_type_id:
                return attr
        return None

    def _get_attribute(self, offset):
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
                self.index,
                self.name_str,
                self.fname_str
            ))

        for attr in self.attributes:
            result = result + "\n\t" + str(attr)

        return result
