# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2014 Darius Bakunas

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
