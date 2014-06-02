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

"""This module is used for partitioning scheme detection (GPT or MBR)

Attributes:
    SCHEME_UNKNOWN (int): When scheme is neither GPT or MBR
    SCHEME_GPT (int): GPT Scheme was identified
    SCHEME_MBR (int): MBR Scheme was indentified
"""

import mbr
import gpt
import struct

SCHEME_UNKNOWN = 0x1
SCHEME_MBR = 0x2
SCHEME_GPT = 0x4


def detect_scheme(filename):
    """Detects partitioning scheme of the source

    Args:
        filename (str): path to file or device for detection of \
        partitioning scheme.

    Returns:
        SCHEME_MBR, SCHEME_GPT or SCHEME_UNKNOWN

    Raises:
        IOError: The file doesn't exist or cannot be opened for reading

    >>> from rawdisk.scheme.common import *
    >>> scheme = detect_scheme('/dev/disk1')
    >>> if (scheme == SCHEME_MBR):
    >>> <...>
    """

    with open(filename, 'rb') as f:
        # Look for MBR signature first
        f.seek(mbr.MBR_SIG_OFFSET)
        data = f.read(mbr.MBR_SIG_SIZE)
        signature = struct.unpack("<H", data)[0]

        if (signature != mbr.MBR_SIGNATURE):
            # Something else
            return SCHEME_UNKNOWN
        else:
            # Could be MBR or GPT, look for GPT header
            f.seek(gpt.GPT_HEADER_OFFSET)
            data = f.read(gpt.GPT_SIG_SIZE)
            signature = struct.unpack("<8s", data)[0]

            if (signature != gpt.GPT_SIGNATURE):
                return SCHEME_MBR
            else:
                return SCHEME_GPT
