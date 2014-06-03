import unittest
from bitstring import pack
from rawdisk.plugins.filesystems.ntfs.ntfs import NtfsPlugin

class TestNtfsPlugin(unittest.TestCase):
    def setUp(self):
        self.filename = 'sample_images/ntfs.vhd'
        self.offset = 0x10000
        self.p = NtfsPlugin()

    def test_detect(self):
        self.assertTrue(self.p.detect(self.filename, self.offset))
        self.assertFalse(self.p.detect(self.filename, self.offset+1))