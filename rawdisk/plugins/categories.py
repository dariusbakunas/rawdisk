# -*- coding: utf-8 -*-


"""This module holds yapsy plugin categories for rawdisk plugins.
Currently only filesystem category plugins are available.
"""

from yapsy.IPlugin import IPlugin


class IFilesystemPlugin(IPlugin):
    """Base abstract class for filesystem plugins.
    """

    @property
    def gpt_identifiers(self):
        """Should return a list (usually one) of GPT identifiers that 
        are used to detect this volume"""
        return []

    @property
    def mbr_identifiers(self):
        """Should return a list (usually one) of MBR identifiers that 
        are used to detect this volume"""
        return []

    @property
    def identifier_string(self):
        mbr_identifiers = map(
            lambda mbr_id: '{:#x}'.format(mbr_id), self.mbr_identifiers)
        gpt_identifiers = map(str, self.gpt_identifiers)

        return 'MBR: [{}], GPT: [{}]'.format(
            ', '.join(mbr_identifiers),', '.join(gpt_identifiers))

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
