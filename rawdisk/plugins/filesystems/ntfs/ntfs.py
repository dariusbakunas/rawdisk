import uuid
import hexdump
import rawdisk.plugins.categories as categories
from ntfs_volume import *
from rawdisk.util.rawstruct import RawStruct
from rawdisk.filesystems.detector import FilesystemDetectorSingleton

SIG_DATA_SIZE = 11
OEM_ID_OFFSET = 0x03


class NtfsPlugin(categories.IFilesystemPlugin):
    def register(self):
        detector = FilesystemDetectorSingleton.get()
        detector.add_mbr_plugin(0x07, self)
        detector.add_gpt_plugin(
            uuid.UUID('{EBD0A0A2-B9E5-4433-87C0-68B6B72699C7}'),
            self
        )

    def detect(self, filename, offset): 
        try:
            with open(filename, 'rb') as f:
                f.seek(offset)
                data = f.read(SIG_DATA_SIZE)
                rs = RawStruct(data)
                oem_id = rs.get_string(OEM_ID_OFFSET, 8)

                if (oem_id == "NTFS    "):
                    return True
        except IOError, e:
            print e

        return None

    def get_volume_object(self):
        return NtfsVolume()