# -*- coding: utf-8 -*-


import os
import rawdisk
import logging
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
        self.logger = logging.getLogger(__name__)
        self.__fs_plugins = []

    def load_plugins(self):
        self.logger.info('Loading filesystem plugins')
        search_path = self.__get_search_path()
        self.__load_filesystem_plugins(search_path=search_path)
        self.__register_filesystem_plugins()

    @property
    def filesystem_plugins(self):
        return self.__fs_plugins

    def __get_search_path(self):
        search_path = [os.path.join(
            os.path.dirname(rawdisk.__file__), "plugins/filesystems"), ]

        search_path += [os.path.join(
            path, APP_NAME, "plugins/filesystems") for path in xdg_data_dirs]

        return search_path

    def __register_filesystem_plugins(self):
        for pluginInfo in self.__fs_plugins:
            self.logger.debug(
                'Registering {} filesystem plugin'.format(pluginInfo.name))

            pluginInfo.plugin_object.register()

    def __load_filesystem_plugins(self, search_path):
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
        self.__fs_plugins = []

        PluginManagerSingleton.setBehaviour([
            VersionedPluginManager,
        ])

        # Load the plugins from the plugin directory.
        plugin_manager = PluginManagerSingleton.get()
        plugin_manager.setPluginPlaces(search_path)
        plugin_manager.setCategoriesFilter({
            "Filesystem": IFilesystemPlugin,
        })

        # Load plugins
        plugin_manager.collectPlugins()

        for pluginInfo in plugin_manager.getPluginsOfCategory("Filesystem"):
            self.__fs_plugins.append(pluginInfo)
