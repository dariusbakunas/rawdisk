# -*- coding: utf-8 -*-


import rawdisk.plugins.categories as categories
import uuid
from rawdisk.filesystems.detector import FilesystemDetector
import rawdisk.plugins.filesystems.efi_system.efi_system_volume as volume

GPT_GUID = '{C12A7328-F81F-11D2-BA4B-00A0C93EC93B}'


class EfiSystem(categories.IFilesystemPlugin):
    """Filesystem plugin for EFI System partition.
    """

    @property
    def gpt_identifiers(self):
        return [GPT_GUID]

    def detect(self, filename, offset, standalone=False):
        """Always returns True, since there is only one partition with this type GUID,
        no need to do further verification.
        """

        if standalone:
            return False

        return True

    def get_volume_object(self):
        """Returns :class:`~.efi_system_volume.EfiSystemVolume`
        object."""
        return volume.EfiSystemVolume()
