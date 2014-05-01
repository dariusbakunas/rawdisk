from rawdisk.util.rawstruct import RawStruct
import hexdump


PART_TYPE_UNKNOWN = 0x00
PART_TYPE_NTFS = 0x01
PART_TYPE_EXFAT = 0x02


def is_type_ntfs(data):
    pt = RawStruct(data)
    oem_id = pt.get_string(3, 8)

    if (oem_id == "NTFS    "):
        return PART_TYPE_NTFS
    else:
        return PART_TYPE_UNKNOWN


def is_type_exfat(data):
    return PART_TYPE_UNKNOWN

type_callbacks = {
    0x7: [is_type_ntfs, is_type_exfat],
}


def detect_partition_type(data, type_id):
    for callback in type_callbacks[type_id]:
        result = callback(data)
        if result != PART_TYPE_UNKNOWN:
            return result

    return PART_TYPE_UNKNOWN


class Partition:
    pass