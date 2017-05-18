import unittest
from rawdisk.session import Session
from rawdisk.scheme.common import SCHEME_MBR
from rawdisk.filesystems.unknown_volume import UnknownVolume


class TestSession(unittest.TestCase):
    def setUp(self):
        self.session = Session()

    def test_load_fileystem_plugins(self):
        self.session.load_plugins()

    def test_load_mbr_without_plugins(self):
        self.session.load(filename='sample_images/ntfs_mbr.vhd')
        self.assertEqual(self.session.partition_scheme, SCHEME_MBR)
        self.assertEqual(len(self.session.volumes), 1)
        self.assertEqual(type(self.session.volumes[0]), UnknownVolume)


