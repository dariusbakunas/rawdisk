import mbr
import gpt
import struct
import hexdump

SCHEME_UNKNOWN = 0x1
SCHEME_MBR = 0x2
SCHEME_GPT = 0x4


def detect_scheme(source):
    """Detects partitioning scheme of the source

    Returns SCHEME_MBR, SCHEME_GPT or SCHEME_UNKNOWN
    """

    # Look for MBR signature first
    source.seek(mbr.MBR_SIG_OFFSET)
    data = source.read(mbr.MBR_SIG_SIZE)
    signature = struct.unpack("<H", data)[0]

    if (signature != mbr.MBR_SIGNATURE):
        # Something else
        return SCHEME_UNKNOWN
    else:
        # Could be MBR or GPT, look for GPT header
        source.seek(gpt.GPT_HEADER_OFFSET)
        data = source.read(gpt.GPT_SIG_SIZE)
        signature = struct.unpack("<8s", data)[0]

        if (signature != gpt.GPT_SIGNATURE):
            return SCHEME_MBR
        else:
            return SCHEME_GPT