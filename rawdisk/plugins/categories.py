# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2004 Darius Bakunas

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

"""This module holds yapsy plugin categories for rawdisk plugins.
Currently only filesystem category plugins are available.
"""

from yapsy.IPlugin import IPlugin


class IFilesystemPlugin(IPlugin):
    """Base abstract class for filesystem plugins.
    """

    def register(self):
        """Call this method to register plugin with :class:`FilesystemDetector \
        <filesystems.detector.FilesystemDetector>`."""
        return

    def detect(self, filename, offset):
        """Method is called by detector for each plugin, that is registered
        with :class:`FilesystemDetector \
        <filesystems.detector.FilesystemDetector>`."""
        return

    def get_volume_object(self):
        """Returns plugin's volume object (inherited from \
            :class:`Volume <filesystems.volume.Volume>`)"""
        return