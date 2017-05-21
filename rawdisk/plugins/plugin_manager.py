# -*- coding: utf-8 -*-


import os
import rawdisk
import logging
from yapsy.PluginManager import PluginManagerSingleton
from yapsy.VersionedPluginManager import VersionedPluginManager
from rawdisk.plugins.categories import IFilesystemPlugin
from xdg.BaseDirectory import xdg_data_dirs

APP_NAME = "rawdisk"


class PluginManager(object):
    """This class is responsible for loading filesystem plugins.

    See Also:
        http://yapsy.sourceforge.net
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def load_filesystem_plugins(self):
        """Looks for *.yapsy-plugin files, loads them and returns a list
            of :class:`VersionedPluginInfo \
            <yapsy.VersionedPluginManager.VersionedPluginInfo>` objects

                Note:
                    Plugin search locations:
                       * $(rawdisk package location)/plugins/filesystems
                       * $(home dir)/.local/share/rawdisk/plugins/filesystems
                       * /usr/local/share/rawdisk/plugins/filesystems
                       * /usr/share/rawdisk/plugins/filesystems
                """
        self.logger.info('Loading filesystem plugins')
        search_path = self.__get_fs_plugin_search_path()
        fs_plugins = []

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
            fs_plugins.append(pluginInfo)

        return fs_plugins

    def __get_fs_plugin_search_path(self):
        search_path = [os.path.join(
            os.path.dirname(rawdisk.__file__), "plugins/filesystems"), ]

        search_path += [os.path.join(
            path, APP_NAME, "plugins/filesystems") for path in xdg_data_dirs]

        return search_path
