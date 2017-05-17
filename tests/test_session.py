import unittest
from rawdisk.session import Session
from rawdisk.scheme.common import SCHEME_MBR


class TestSession(unittest.TestCase):
    def setUp(self):
        self.session = Session()

    def test_load_mbr(self):
        self.session.load(filename='sample_images/ntfs_mbr.vhd')
        self.assertEquals(self.session.partition_scheme, SCHEME_MBR)
        self.assertEquals(len(self.session.volumes), 1)
