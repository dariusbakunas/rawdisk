# -*- coding: utf-8 -*-


import os
import rawdisk
from yapsy.PluginManager import PluginManagerSingleton
from yapsy.VersionedPluginManager import VersionedPluginManager
from rawdisk.plugins.categories import IFilesystemPlugin
from xdg.BaseDirectory import xdg_data_dirs

APP_NAME = "rawdisk"


class Manager(object):
    """This class is responsible for loading filesystem plugins.

    See Also:
        http://yapsy.sourceforge.net
    """

    def __init__(self):
        self.fs_plugins = []
        self.search_path = []

    def load_plugins(self):
        self._initialize_search_path()
        self._load_filesystem_plugins()
        self._register_filesystem_plugins()

    def _initialize_search_path(self):
        self.search_path = [os.path.join(
            os.path.dirname(rawdisk.__file__), "plugins/filesystems"), ]
        [self.search_path.append(
            os.path.join(path, APP_NAME, "plugins/filesystems")
        )
            for path in xdg_data_dirs]

    def _register_filesystem_plugins(self):
        for pluginInfo in self.fs_plugins:
            pluginInfo.plugin_object.register()

    def _load_filesystem_plugins(self):
        # import logging
        # logging.basicConfig(level=logging.DEBUG)

        """Looks for *.yapsy-plugin files and loads them. It calls 'register' \
        method for each plugin, which in turn registers with \
        :class:`FilesystemDetector \
        <rawdisk.filesystems.detector.FilesystemDetector>`.

        Note:
            Plugin search locations:
               * $(rawdisk package location)/plugins/filesystems
               * $(home dir)/.local/share/rawdisk/plugins/filesystems
               * /usr/local/share/rawdisk/plugins/filesystems
               * /usr/share/rawdisk/plugins/filesystems
        """
        PluginManagerSingleton.setBehaviour([
            VersionedPluginManager,
        ])

        # Load the plugins from the plugin directory.
        self.manager = PluginManagerSingleton.get()
        self.manager.setPluginPlaces(self.search_path)
        self.manager.setCategoriesFilter({
            "Filesystem": IFilesystemPlugin,
        })

        # Load plugins
        self.manager.collectPlugins()

        for pluginInfo in self.manager.getPluginsOfCategory("Filesystem"):
            self.fs_plugins.append(pluginInfo)
