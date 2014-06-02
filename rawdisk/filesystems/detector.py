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

"""This module is mostly used by plugins to register filesystem
detection routines that are internaly used by rawdisk.reader.Reader
to match filesystems"""


class FilesystemDetector(object):
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


class FilesystemDetectorSingleton(object):
    """Singleton implementation for FilesystemDetector
    """

    __instance = None

    def __init__(self):
        if self.__instance is not None:
            raise Exception("Singleton can't be created twice !")

    @classmethod
    def get(self):
        """Returns singleton version of FilesystemDetector,
        so that all plugins could use the same instance for registration

        Returns:
            Singleton FilesystemDetector object
        """
        if self.__instance is None:
            self.__instance = FilesystemDetector()

        return self.__instance