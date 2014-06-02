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
from rawdisk.filesystems.detector import FilesystemDetectorSingleton
import rawdisk.plugins.filesystems.efi_system.efi_system_volume as volume


class EfiSystemPlugin(categories.IFilesystemPlugin):
    """Filesystem plugin for EFI System partition.
    """
    def register(self):
        """Registers this plugin with :class:`FilesystemDetector \
        <filesystems.detector.FilesystemDetector>` as gpt plugin, \
        with type guid *{C12A7328-F81F-11D2-BA4B-00A0C93EC93B}*
        """
        detector = FilesystemDetectorSingleton.get()
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
        """Returns :class:`EfiSystemVolume \
        <plugins.filesystems.efi_system.efi_system_volume.EfiSystemVolume>` \
        object."""
        return volume.EfiSystemVolume()