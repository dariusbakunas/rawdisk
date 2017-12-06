import unittest
from rawdisk.plugins.filesystems.ext2.ext2 import Ext2


class TestExt2Plugin(unittest.TestCase):
    def setUp(self):
        self.filename = 'sample_images/ext2_mbr.img'
        self.plugin = Ext2()
        self.offset = 1048576

    def test_detect(self):
        self.assertTrue(self.plugin.detect(self.filename, self.offset))
