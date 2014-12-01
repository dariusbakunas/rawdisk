# -*- coding: utf-8 -*-
from ctypes import Structure, c_ushort, c_ubyte, c_uint, c_ulonglong, \
    c_byte


class BIOS_PARAMETER_BLOCK(Structure):
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
        ("checksum",            c_uint),
    ]
