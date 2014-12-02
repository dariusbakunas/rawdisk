# -*- coding: utf-8 -*-
from ctypes import Structure, c_ushort, c_ubyte, c_uint, c_ulonglong, \
    c_byte, c_char


class BIOS_PARAMETER_BLOCK(Structure):
    """Bios parameter block.

    Attributes:
        bytes_per_sector (ushort): Sector size with which the physical \
        disc medium has been low-level formatted in bytes.
        sectors_per_cluster (ubyte): Number of sectors in an allocation unit.
        reserved_sectors (ushort): Number of sectors in the area at the start \
        of the volume that is reserved for operating system boot code.
        media_descriptor (ubyte): Describes type of device used eg. floppy,
        harddisk (not used anymore?).
        total_sectors (ulonglong): Total number of sectors in the volume.
        mft_cluster (ulonglong): MFT table first cluster number \
        (*mft offset = volume offset + bytes_per_sector * \
            sectors_per_cluster * mft_cluster*).
        mft_mirror_cluster (ulonglong): Mirror MFT table cluster number.
        clusters_per_mft (signed char): MFT record size. \
        Per Microsoft: If this number is positive (up to 0x7F), it represents \
        Clusters per MFT record. If the number is negative (0x80 to 0xFF), \
        the size of the File Record is 2 raised to the absolute value of \
        this number.
        clusters_per_index (uint): Index block size.
        volume_serial (ulonglong): Volume serial number.
        checksum (uint): BPB checksum.

    See More:
        | http://en.wikipedia.org/wiki/BIOS_parameter_block
        | http://ntfs.com/ntfs-partition-boot-sector.htm
    """
    _fields_ = [
        ("bytes_per_sector",    c_ushort),
        ("sectors_per_cluster", c_ubyte),
        ("reserved_sectors",    c_ushort),
        ("media_type",          c_ubyte),
        ("sectors_per_track",   c_ushort),
        ("heads",               c_ushort),
        ("hidden_sectors",      c_uint),
        ("total_sectors",       c_ulonglong),
    ]


class EXTENDED_BIOS_PARAMETER_BLOCK(Structure):
    _fields_ = [
        ("mft_cluster",         c_ulonglong),
        ("mft_mirror_cluster",  c_ulonglong),
        ("clusters_per_mft",    c_byte),
        ("clusters_per_index",  c_ubyte),
        ("volume_serial",       c_ulonglong),
    ]


class MFT_RECORD_HEADER(Structure):
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
    _fields_ = [
        ("signature",               c_char * 4),
        ("upd_seq_array_offset",    c_ushort),
        ("upd_seq_array_size",      c_ushort),
        ("logfile_seq_number",      c_ulonglong),
        ("seq_number",              c_ushort),
        ("hard_link_count",         c_ushort),
        ("first_attr_offset",       c_ushort),
        ("flags",                   c_ushort),
        ("used_size",               c_uint),
        ("allocated_size",          c_ushort),
        ("base_file_record",        c_ulonglong),
        ("next_attr_id",            c_ushort),
        ("mft_record_number",       c_uint),
    ]
