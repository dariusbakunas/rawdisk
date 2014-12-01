# -*- coding: utf-8 -*-
from ctypes import *

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
