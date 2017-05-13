import unittest
from rawdisk.reader import Reader
from rawdisk.scheme.common import SCHEME_MBR


class TestReader(unittest.TestCase):
    def setUp(self):
        self.reader = Reader()

    def test_load_mbr(self):
        self.reader.load(filename='sample_images/ntfs_mbr.vhd')
        self.assertEquals(self.reader.scheme, SCHEME_MBR)
        self.assertEquals(len(self.reader.partitions), 1)
