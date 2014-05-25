from rawdisk.util.rawstruct import RawStruct
from rawdisk.filesystems.detector import FilesystemDetectorSingleton
from hfs_plus_volume import *
import rawdisk.plugins.categories as categories
import uuid


class HfsPlusPlugin(categories.IFilesystemPlugin):
    def register(self):
        detector = FilesystemDetectorSingleton.get()
        detector.add_gpt_plugin(
            uuid.UUID('{48465300-0000-11AA-AA11-00306543ECAC}'),
            self
        )

    def detect(self, filename, offset): 
        # There is no need to check since matching
        # by guid in this case is enough
        return True

    def get_volume_object(self):
        return HfsPlusVolume()