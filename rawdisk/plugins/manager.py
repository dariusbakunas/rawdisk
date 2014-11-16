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

    @staticmethod
    def load_filesystem_plugins():
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
        manager = PluginManagerSingleton.get()

        places = [os.path.join(
            os.path.dirname(rawdisk.__file__), "plugins/filesystems"), ]
        [places.append(os.path.join(path, APP_NAME, "plugins/filesystems"))
            for path in xdg_data_dirs]

        manager.setPluginPlaces(places)
        manager.setCategoriesFilter({
            "Filesystem": IFilesystemPlugin,
        })

        # Load plugins
        manager.collectPlugins()

        for pluginInfo in manager.getPluginsOfCategory("Filesystem"):
            pluginInfo.plugin_object.register()
