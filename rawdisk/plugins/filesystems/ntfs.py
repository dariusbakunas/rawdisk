import uuid
import rawdisk.plugins.categories as categories
from rawdisk.filesystems.detector import FilesystemDetectorSingleton
from rawdisk.util.rawstruct import RawStruct
from rawdisk.filesystems.ntfs import NtfsVolume

SIG_DATA_SIZE = 512

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
                oem_id = rs.get_string(0x03, 8)

                if (oem_id == "NTFS    "):
                    return True
        except IOError, e:
            print e

        return None

    def get_volume_object(self):
        return NtfsVolume()