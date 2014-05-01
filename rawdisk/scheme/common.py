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

    Returns SCHEME_MBR, SCHEME_GPT or SCHEME_UNKNOWN
    """

    try:
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
    except IOError, e:
        print e    
