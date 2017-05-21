# -*- coding: utf-8 -*-
"""
Linux Ext2 volume:

offset  size   description
--------------------------
0x0     1024   boot block (unused)
0x400   1024   superblock

"""


import rawdisk.plugins.categories as categories
from rawdisk.util.rawstruct import RawStruct
from rawdisk.plugins.filesystems.ext2.superblock import SuperBlock
from rawdisk.plugins.filesystems.ext2.ext2_volume import Ext2Volume


MBR_ID = 0x83


class Ext2(categories.IFilesystemPlugin):
    """Plugin for Linux partition(s)"""

    @property
    def mbr_identifiers(self):
        return [MBR_ID]

    def detect(self, filename, offset):
        sb = SuperBlock(
            filename=filename,
            offset=offset + 1024,
            length=1024)

        if sb.magic == 0xef53:
            # ext2
            return True

        return False

    def get_volume_object(self):
        return Ext2Volume()
