from rawdisk.util.rawstruct import RawStruct
import hexdump
import uuid


PART_FORMAT_UNKNOWN = 0x00
PART_FORMAT_NTFS = 0x01
PART_FORMAT_EXFAT = 0x02
PART_FORMAT_HFS_PLUS = 0x03;


def is_type_ntfs(data):
    pt = RawStruct(data)
    oem_id = pt.get_string(3, 8)

    if (oem_id == "NTFS    "):
        return PART_FORMAT_NTFS
    else:
        return PART_FORMAT_UNKNOWN


def is_type_exfat(data):
    return PART_FORMAT_UNKNOWN

type_callbacks = {
    0x7: [is_type_ntfs, is_type_exfat],
}

def detect_gpt_partition_format(type_guid):
    if type_guid == uuid.UUID('{48465300-0000-11AA-AA11-00306543ECAC}'):
        return PART_FORMAT_HFS_PLUS
    else:
        return PART_FORMAT_UNKNOWN

def detect_mbr_partition_format(filename, offset, type_id):
    data = None

    try:
        with open(filename, 'rb') as f:
            f.seek(offset)
            data = f.read(512)  # not sure yet if 512 is enough

            for callback in type_callbacks[type_id]:
                result = callback(data)
                if result != PART_FORMAT_UNKNOWN:
                    return result
    except IOError, e:
        print e

    return PART_FORMAT_UNKNOWN