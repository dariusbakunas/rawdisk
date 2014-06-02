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
        :class:`FilesystemDetector <filesystems.detector.FilesystemDetector>`.

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