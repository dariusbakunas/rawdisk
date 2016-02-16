# -*- coding: utf-8 -*-
"""
Linux Ext2 volume:

offset  size   description
--------------------------
0x0     1024   boot block (unused)
0x400   1024   superblock

"""

import rawdisk.plugins.categories as categories
from rawdisk.filesystems.detector import FilesystemDetector
from rawdisk.util.rawstruct import RawStruct


class SuperBlock(RawStruct):
    """
    Ext2 (and probably other ExtN) superblock.
    See http://wiki.osdev.org/Ext2#Superblock
    """
    def __init__(self, **kwargs):
        RawStruct.__init__(self, **kwargs)

        self.inodes_count = self.get_uint_le(0)
        self.iblocks_count = self.get_uint_le(4)
        self.reserved_blocks_count = self.get_uint_le(8)
        self.free_blocks_count = self.get_uint_le(12)
        self.free_inodes_count = self.get_uint_le(16)
        self.first_data_block = self.get_uint_le(20)
        self.log_block_size = self.get_uint_le(24)

        self.log_fragment_size = self.get_int_le(28)

        self.blocks_per_group = self.get_uint_le(32)
        self.fragments_per_group = self.get_uint_le(36)
        self.inodes_per_group = self.get_uint_le(40)
        self.mtime = self.get_uint_le(44)
        self.wtime = self.get_uint_le(48)

        self.mount_count = self.get_ushort_le(52)
        self.max_mount_count = self.get_ushort_le(54)
        self.magic = self.get_ushort_le(56)
        self.state = self.get_ushort_le(58)
        self.errors = self.get_ushort_le(60)
        self.minor_revision_level = self.get_ushort_le(62)

        self.lastcheck = self.get_uint_le(64)
        self.checkinterval = self.get_uint_le(68)
        self.creator_os = self.get_uint_le(72)
        self.revision_level = self.get_uint_le(76)

        self.default_resuid = self.get_ushort_le(80)
        self.default_resgid = self.get_ushort_le(82)


class LinuxPlugin(categories.IFilesystemPlugin):
    """Plugin for Linux partition(s)"""

    def register(self):
        """Registers as mbr plugin for partition type 0x83 """
        detector = FilesystemDetector()
        detector.add_mbr_plugin(0x83, self)

    def detect(self, filename, offset):
        sb = SuperBlock(
            filename=filename,
            offset=offset + 1024,
            length=1024)

        if sb.magic == 0xef53:
            # ext2
            return True

        return False
