import unittest
import uuid
from rawdisk.plugins.filesystems.ntfs.ntfs import NtfsPlugin
from rawdisk.plugins.filesystems.ntfs.bpb import Bpb
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

class TestBpb(unittest.TestCase):
    def setUp(self):
        with open('sample_images/ntfs_bpb.bin', 'r') as f:
            self.data = f.read()

    def test_init(self):
        bpb = Bpb(self.data)
        self.assertEquals(bpb.bytes_per_sector, 512)
        self.assertEquals(bpb.sectors_per_cluster, 8)
        self.assertEquals(bpb.reserved_sectors, 0)
        self.assertEquals(bpb.media_descriptor, 0xF8)
        self.assertEquals(bpb.sectors_per_track, 0x3F)
        self.assertEquals(bpb.number_of_heads, 0xFF)
        self.assertEquals(bpb.total_sectors, 0x1FE7FF)
        self.assertEquals(bpb.mft_cluster, 0x15455)
        self.assertEquals(bpb.mft_mirror_cluster, 0x2)
        self.assertEquals(bpb.clusters_per_mft, 0xF6)
        self.assertEquals(bpb.clusters_per_index, 0x1)
        self.assertEquals(bpb.volume_serial, 0xa028d573cf000000L)
        self.assertEquals(bpb.checksum, 0xE228D5)
        self.assertEquals(bpb.mft_offset, 0x15455000)
        self.assertEquals(bpb.mft_mirror_offset, 0x2000)