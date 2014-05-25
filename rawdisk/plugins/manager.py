import os
import rawdisk
from yapsy.PluginManager import PluginManagerSingleton
from yapsy.VersionedPluginManager import VersionedPluginManager
from rawdisk.plugins.categories import IFilesystemPlugin
from xdg.BaseDirectory import xdg_data_dirs

APP_NAME = "rawdisk"

class Manager(object):
    @staticmethod
    def load_filesystem_plugins():
        PluginManagerSingleton.setBehaviour([
            VersionedPluginManager,
        ])

        # Load the plugins from the plugin directory.
        manager = PluginManagerSingleton.get()

        places = [os.path.dirname(rawdisk.__file__),]
        [places.append(os.path.join(path, APP_NAME, "plugins/filesystems")) for path in xdg_data_dirs]

        manager.setPluginPlaces(places)
        manager.setCategoriesFilter({
            "Filesystem" : IFilesystemPlugin,
        })

        # Load plugins
        manager.collectPlugins()

        for pluginInfo in manager.getPluginsOfCategory("Filesystem"):
            pluginInfo.plugin_object.register()