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

import uuid
import rawdisk.plugins.categories as categories
from rawdisk.plugins.filesystems.ntfs.ntfs_volume import NtfsVolume
from rawdisk.util.rawstruct import RawStruct
from rawdisk.filesystems.detector import FilesystemDetectorSingleton

SIG_DATA_SIZE = 11
OEM_ID_OFFSET = 0x03


class NtfsPlugin(categories.IFilesystemPlugin):
    """Filesystem plugin for NTFS partition.
    """
    def register(self):
        """Registers this plugin with :class:`FilesystemDetector \
        <filesystems.detector.FilesystemDetector>` as gpt plugin, \
        with type guid *{EBD0A0A2-B9E5-4433-87C0-68B6B72699C7}* and \
        as mbr plugin with type id 0x07
        """
        detector = FilesystemDetectorSingleton.get()
        detector.add_mbr_plugin(0x07, self)
        detector.add_gpt_plugin(
            uuid.UUID('{EBD0A0A2-B9E5-4433-87C0-68B6B72699C7}'),
            self
        )

    def detect(self, filename, offset):
        """Verifies NTFS filesystem signature.

        Returns:
            bool: True if filesystem signature at offset 0x03 \
            matches 'NTFS    ', False otherwise.
        """
        try:
            with open(filename, 'rb') as f:
                f.seek(offset)
                data = f.read(SIG_DATA_SIZE)
                rs = RawStruct(data)
                oem_id = rs.get_string(OEM_ID_OFFSET, 8)

                if (oem_id == "NTFS    "):
                    return True
        except IOError, e:
            print e

        return None

    def get_volume_object(self):
        """Returns :class:`NtfsVolume \
        <plugins.filesystems.ntfs.ntfs_volume.NtfsVolume>` object."""
        return NtfsVolume()