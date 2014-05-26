from rawdisk.util.rawstruct import RawStruct
from rawdisk.filesystems.detector import FilesystemDetectorSingleton
from apple_boot_volume import *
import rawdisk.plugins.categories as categories
import uuid


class AppleBootPlugin(categories.IFilesystemPlugin):
    def register(self):
        detector = FilesystemDetectorSingleton.get()
        detector.add_gpt_plugin(
            uuid.UUID('{426f6f74-0000-11aa-aa11-00306543ecac}'),
            self
        )

    def detect(self, filename, offset): 
        # There is no need to check since matching
        # by guid in this case is enough
        return True

    def get_volume_object(self):
        return AppleBootVolume()