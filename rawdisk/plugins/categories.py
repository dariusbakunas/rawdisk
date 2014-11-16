# -*- coding: utf-8 -*-


"""This module holds yapsy plugin categories for rawdisk plugins.
Currently only filesystem category plugins are available.
"""

from yapsy.IPlugin import IPlugin


class IFilesystemPlugin(IPlugin):
    """Base abstract class for filesystem plugins.
    """

    def register(self):
        """Call this method to register plugin with :class:`FilesystemDetector \
        <rawdisk.filesystems.detector.FilesystemDetector>`."""
        return

    def detect(self, filename, offset):
        """Method is called by detector for each plugin, that is registered
        with :class:`FilesystemDetector \
        <rawdisk.filesystems.detector.FilesystemDetector>`."""
        return

    def get_volume_object(self):
        """Returns plugin's volume object (inherited from \
            :class:`Volume <rawdisk.filesystems.volume.Volume>`)"""
        return
