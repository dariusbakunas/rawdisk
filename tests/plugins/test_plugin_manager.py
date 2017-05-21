import unittest
from rawdisk.plugins.plugin_manager import PluginManager


class PluginManagerModuleTest(unittest.TestCase):
    def setUp(self):
        self.manager = PluginManager()

    def test_load_plugins(self):
        plugins = self.manager.load_filesystem_plugins()
        self.assertEqual(len(plugins), 5)
