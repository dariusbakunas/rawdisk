import unittest
import uuid
from rawdisk.plugins.filesystems.ntfs.ntfs import NtfsPlugin
from rawdisk.filesystems.detector import FilesystemDetector


class TestNtfsPlugin(unittest.TestCase):
    def setUp(self):
        self.filename = 'sample_images/ntfs.vhd'
        self.offset = 0x10000
        self.p = NtfsPlugin()
        self.detector = FilesystemDetector()

    def test_detect(self):
        self.assertTrue(self.p.detect(self.filename, self.offset))
        self.assertFalse(self.p.detect(self.filename, self.offset+1))

    def test_register(self):
        self.p.register()

        mbr_plugins = self.detector.mbr_plugins.get(0x07)
        gpt_plugins = self.detector.gpt_plugins.get(
            uuid.UUID('{EBD0A0A2-B9E5-4433-87C0-68B6B72699C7}')
        )

        self.assertEquals(len(mbr_plugins), 1)
        self.assertEquals(len(gpt_plugins), 1)

    def tearDown(self):
        # drop the singleton
        self.detector._clear_plugins()