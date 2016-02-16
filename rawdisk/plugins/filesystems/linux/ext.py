# -*- coding: utf-8 -*-

import rawdisk.plugins.categories as categories
from rawdisk.filesystems.detector import FilesystemDetector


class LinuxPlugin(categories.IFilesystemPlugin):
    """Plugin for Linux partition(s)"""

    def register(self):
        """Registers as mbr plugin for partition type 0x83 """
        detector = FilesystemDetector()
        detector.add_mbr_plugin(0x83, self)

    def detect(self, filename, offset):
        return False
