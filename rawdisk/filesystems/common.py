from rawdisk.util.rawstruct import RawStruct
import hexdump
import uuid

# Not sure if this is enough
SIG_DATA_SIZE = 512

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

def detect_gpt_partition_format(filename, offset, type_guid):
    if type_guid == uuid.UUID('{48465300-0000-11AA-AA11-00306543ECAC}'):
        return PART_FORMAT_HFS_PLUS
    elif type_guid == uuid.UUID('{EBD0A0A2-B9E5-4433-87C0-68B6B72699C7}'):
        # Basic data partition
        try:
            with open(filename, 'rb') as f:
                f.seek(offset)
                data = f.read(SIG_DATA_SIZE)
                
                # TODO: 
                # According to Microsoft, the basic data partition 
                # is the equivalent to partition types 0x06, 0x07, and 0x0B
                # callbacks = []
                # callbacks.append(type_callbacks[0x06])
                # callbacks.append(type_callbacks[0x07])
                # callbacks.append(type_callbacks[0x0B])
                for callback in type_callbacks[0x07]:
                    result = callback(data)
                    if result != PART_FORMAT_UNKNOWN:
                        return result
        except IOError, e:
            print e
    else:
        return PART_FORMAT_UNKNOWN

def detect_mbr_partition_format(filename, offset, type_id):
    data = None

    try:
        with open(filename, 'rb') as f:
            f.seek(offset)
            data = f.read(SIG_DATA_SIZE)

            for callback in type_callbacks[type_id]:
                result = callback(data)
                if result != PART_FORMAT_UNKNOWN:
                    return result
    except IOError, e:
        print e

    return PART_FORMAT_UNKNOWN