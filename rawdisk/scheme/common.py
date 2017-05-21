# -*- coding: utf-8 -*-


"""This module is used for partitioning scheme detection (GPT or MBR)

Attributes:
    SCHEME_UNKNOWN (int): When scheme is neither GPT or MBR
    SCHEME_GPT (int): GPT Scheme was identified
    SCHEME_MBR (int): MBR Scheme was indentified
"""
import struct
import logging
from enum import Enum
from rawdisk.scheme import mbr
from rawdisk.scheme import gpt

class PartitionScheme(Enum):
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
    >>> if scheme == PartitionScheme.SCHEME_MBR:
    >>> <...>
    """

    logger = logging.getLogger(__name__)
    logger.info('Detecting partitioning scheme')

    with open(filename, 'rb') as f:
        # Look for MBR signature first
        f.seek(mbr.MBR_SIG_OFFSET)
        data = f.read(mbr.MBR_SIG_SIZE)
        signature = struct.unpack("<H", data)[0]

        if signature != mbr.MBR_SIGNATURE:
            # Something else
            logger.debug('Unknown partitioning scheme')
            return PartitionScheme.SCHEME_UNKNOWN
        else:
            # Could be MBR or GPT, look for GPT header
            f.seek(gpt.GPT_HEADER_OFFSET)
            data = f.read(gpt.GPT_SIG_SIZE)
            signature = struct.unpack("<8s", data)[0]

            if signature != gpt.GPT_SIGNATURE:
                logger.debug('MBR scheme detected')
                return PartitionScheme.SCHEME_MBR
            else:
                logger.debug('GPT scheme detected')
                return PartitionScheme.SCHEME_GPT
