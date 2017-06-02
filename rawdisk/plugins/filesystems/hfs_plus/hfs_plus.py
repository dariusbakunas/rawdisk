# -*- coding: utf-8 -*-


import rawdisk.plugins.categories as categories
import uuid
from rawdisk.filesystems.detector import FilesystemDetector
from rawdisk.plugins.filesystems.hfs_plus.hfs_plus_volume import HfsPlusVolume

GPT_GUID = '{48465300-0000-11AA-AA11-00306543ECAC}'


class HfsPlus(categories.IFilesystemPlugin):
    """Filesystem plugin for HFS+ partition.
    """

    @property
    def gpt_identifiers(self):
        return [GPT_GUID]

    def detect(self, filename, offset, standalone=False):
        """Always returns True, since there is only one partition with \
        this type GUID, no need to do further verification.
        """
        if standalone:
            return False

        return True

    def get_volume_object(self):
        """Returns :class:`~.hfs_plus_volume.HfsPlusVolume` object."""
        return HfsPlusVolume()
