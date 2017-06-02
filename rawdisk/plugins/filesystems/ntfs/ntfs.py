# -*- coding: utf-8 -*-


import uuid
import rawdisk.plugins.categories as categories
from rawdisk.util.rawstruct import RawStruct
from rawdisk.plugins.filesystems.ntfs.ntfs_volume import NtfsVolume
from rawdisk.filesystems.detector import FilesystemDetector

SIG_SIZE = 8
SIG_OFFSET = 0x03

MBR_ID = 0x07
GPT_GUID = '{EBD0A0A2-B9E5-4433-87C0-68B6B72699C7}'


class Ntfs(categories.IFilesystemPlugin):
    """Filesystem plugin for NTFS partition.
    """

    @property
    def mbr_identifiers(self):
        return [MBR_ID]

    @property
    def gpt_identifiers(self):
        return [GPT_GUID]

    def detect(self, filename, offset, standalone=False):
        """Verifies NTFS filesystem signature.

        Returns:
            bool: True if filesystem signature at offset 0x03 \
            matches 'NTFS    ', False otherwise.
        """
        r = RawStruct(
            filename=filename,
            offset=offset + SIG_OFFSET,
            length=SIG_SIZE)

        oem_id = r.data

        if oem_id == b"NTFS    ":
            return True

        return False

    def get_volume_object(self):
        """Returns :class:`~.ntfs_volume.NtfsVolume` object."""
        return NtfsVolume()
