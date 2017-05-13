import unittest
from rawdisk.plugins.manager import Manager


class ManagerModuleTest(unittest.TestCase):
    def setUp(self):
        self.manager = Manager()

    def test_load_plugins(self):
        self.manager.load_plugins()
        self.assertEqual(len(self.manager.fs_plugins), 4)
