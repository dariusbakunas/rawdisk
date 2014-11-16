# -*- coding: utf-8 -*-


import rawdisk.plugins.categories as categories
import uuid
from rawdisk.filesystems.detector import FilesystemDetector
import rawdisk.plugins.filesystems.efi_system.efi_system_volume as volume


class EfiSystemPlugin(categories.IFilesystemPlugin):
    """Filesystem plugin for EFI System partition.
    """
    def register(self):
        """Registers this plugin with \
        :class:`~rawdisk.filesystems.detector.FilesystemDetector` \
        as gpt plugin, with type guid *{C12A7328-F81F-11D2-BA4B-00A0C93EC93B}*
        """
        detector = FilesystemDetector()
        detector.add_gpt_plugin(
            uuid.UUID('{C12A7328-F81F-11D2-BA4B-00A0C93EC93B}'),
            self
        )

    def detect(self, filename, offset):
        """Always returns True, since there is only one partition with this type GUID,
        no need to do further verification.
        """
        return True

    def get_volume_object(self):
        """Returns :class:`~.efi_system_volume.EfiSystemVolume`
        object."""
        return volume.EfiSystemVolume()
