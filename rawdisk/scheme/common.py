# Copyright (c) 2009, David Buxton <david@gasmark6.com>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""This module is used for partitioning scheme detection (GPT or MBR)

Attributes:
    SCHEME_UNKNOWN (int): When scheme is neither GPT or MBR
    SCHEME_GPT (int): GPT Scheme was identified
    SCHEME_MBR (int): MBR Scheme was indentified
"""

import mbr
import gpt
import struct
import hexdump
import sys

SCHEME_UNKNOWN = 0x1
SCHEME_MBR = 0x2
SCHEME_GPT = 0x4


def detect_scheme(filename):
    """Detects partitioning scheme of the source

    Args:
        filename (str): path to file or device for detection of partitioning scheme

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
