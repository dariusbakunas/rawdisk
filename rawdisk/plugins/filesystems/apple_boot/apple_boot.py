# -*- coding: utf-8 -*-


import rawdisk.plugins.categories as categories
import uuid
from rawdisk.filesystems.detector import FilesystemDetector
import rawdisk.plugins.filesystems.apple_boot.apple_boot_volume as volume

GPT_GUID = '{426f6f74-0000-11aa-aa11-00306543ecac}'


class AppleBoot(categories.IFilesystemPlugin):
    """Filesystem plugin for Apple_Boot partition.
    """
    @property
    def gpt_identifiers(self):
        return [GPT_GUID]

    def register(self):
        """Registers this plugin with \
        :class:`~rawdisk.filesystems.detector.FilesystemDetector` \
        as gpt plugin, with type guid *{426f6f74-0000-11aa-aa11-00306543ecac}*
        """
        detector = FilesystemDetector()
        detector.add_gpt_plugin(
            uuid.UUID(GPT_GUID),
            self
        )

    def detect(self, filename, offset):
        """Always returns True, since there is only one partition \
        with this type GUID, no need to do further verification.
        """
        return True

    def get_volume_object(self):
        """Returns :class:`~.apple_boot_volume.AppleBootVolume` \
        object."""
        return volume.AppleBootVolume()
