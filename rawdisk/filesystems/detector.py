# -*- coding: utf-8 -*-

"""This module is mostly used by plugins to register filesystem
detection routines that are internaly used by rawdisk.reader.Reader
to match filesystems"""

from rawdisk.util.singleton import Singleton


class FilesystemDetector(object, metaclass=Singleton):
    """A class that allows to match filesystem id or guid against available
    plugins.

    Warning:
        Do not use this class directly, use
        :class:`FilesystemDetectorSingleton` instead
    """
    def __init__(self):
        # 2 dimensional array of fs_id : [list of plugins]
        self.mbr_plugins = {}
        # 2 dimensional array of fs_guid : [list of plugins]
        self.gpt_plugins = {}

    def _clear_plugins(self):
        self.mbr_plugins.clear()
        self.gpt_plugins.clear()

    def add_mbr_plugin(self, fs_id, plugin):
        """Used in plugin's registration routine,
        to associate it's detection method with given filesystem id

        Args:
            fs_id: filesystem id that is read from MBR partition entry
            plugin: plugin that supports this filesystem
        """

        if fs_id in self.mbr_plugins:
            self.mbr_plugins.get(fs_id).append(plugin)
        else:
            self.mbr_plugins[fs_id] = [plugin, ]

    def add_gpt_plugin(self, fs_guid, plugin):
        """Used in plugin's registration routine,
        to associate it's detection method with given filesystem guid

        Args:
            fs_guid: filesystem guid that is read from GPT partition entry
            plugin: plugin that supports this filesystem
        """
        if fs_guid in self.gpt_plugins:
            self.gpt_plugins.get(fs_guid).append(plugin)
        else:
            self.gpt_plugins[fs_guid] = [plugin, ]

    def detect_mbr(self, filename, offset, fs_id):
        """Used by rawdisk.reader.Reader to match mbr partitions agains
        filesystem plugins.

        Args:
            filename: device or file that it will read in order to detect
            the filesystem fs_id: filesystem id to match (ex. 0x07)
            offset: offset for the filesystem that is being matched

        Returns:
            Volume object supplied by matched plugin.
            If there is no match, None is returned
        """
        if fs_id not in self.mbr_plugins:
            return None
        else:
            plugins = self.mbr_plugins.get(fs_id)
            for plugin in plugins:
                if plugin.detect(filename, offset):
                    return plugin.get_volume_object()
        return None

    def detect_gpt(self, filename, offset, fs_guid):
        """Used by rawdisk.reader.Reader to match gpt partitions agains
        filesystem plugins.

        Args:
            filename: device or file that it will read in order to detect the
            filesystem
            fs_id: filesystem guid to match
            (ex. {EBD0A0A2-B9E5-4433-87C0-68B6B72699C7})
            offset: offset for the filesystem that is being matched

        Returns:
            Volume object supplied by matched plugin.
            If there is no match, None is returned
        """
        if fs_guid not in self.gpt_plugins:
            return None
        else:
            plugins = self.gpt_plugins.get(fs_guid)
            for plugin in plugins:
                if plugin.detect(filename, offset):
                    return plugin.get_volume_object()

        return None
