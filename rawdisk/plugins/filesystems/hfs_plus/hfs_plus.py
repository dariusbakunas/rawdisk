# -*- coding: utf-8 -*-


import rawdisk.plugins.categories as categories
import uuid
from rawdisk.filesystems.detector import FilesystemDetector
from rawdisk.plugins.filesystems.hfs_plus.hfs_plus_volume import HfsPlusVolume


class HfsPlusPlugin(categories.IFilesystemPlugin):
    """Filesystem plugin for HFS+ partition.
    """
    def register(self):
        """Registers this plugin with \
        :class:`~rawdisk.filesystems.detector.FilesystemDetector` \
        as gpt plugin, with type guid *{48465300-0000-11AA-AA11-00306543ECAC}*
        """
        detector = FilesystemDetector()
        detector.add_gpt_plugin(
            uuid.UUID('{48465300-0000-11AA-AA11-00306543ECAC}'),
            self
        )

    def detect(self, filename, offset):
        """Always returns True, since there is only one partition with \
        this type GUID, no need to do further verification.
        """
        return True

    def get_volume_object(self):
        """Returns :class:`~.hfs_plus_volume.HfsPlusVolume` object."""
        return HfsPlusVolume()
