from rawdisk.util.rawstruct import RawStruct
from rawdisk.filesystems.detector import FilesystemDetectorSingleton
from efi_system_volume import *
import rawdisk.plugins.categories as categories
import uuid


class EfiSystemPlugin(categories.IFilesystemPlugin):
    def register(self):
        detector = FilesystemDetectorSingleton.get()
        detector.add_gpt_plugin(
            uuid.UUID('{C12A7328-F81F-11D2-BA4B-00A0C93EC93B}'),
            self
        )

    def detect(self, filename, offset): 
        # There is no need to check since matching
        # by guid in this case is enough
        return True

    def get_volume_object(self):
        return EfiSystemVolume()