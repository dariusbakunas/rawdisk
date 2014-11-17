#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import uuid
from rawdisk.plugins.filesystems.ntfs.ntfs import NtfsPlugin
from rawdisk.plugins.filesystems.ntfs.bpb import Bpb, BPB_OFFSET
from rawdisk.plugins.filesystems.ntfs.bootsector import BootSector
from rawdisk.plugins.filesystems.ntfs.mft import MftTable
from rawdisk.plugins.filesystems.ntfs.ntfs_volume import NtfsVolume, \
    NUM_SYSTEM_ENTRIES
from rawdisk.filesystems.detector import FilesystemDetector

#These are real values for the sample 'ntfs_mbr.vhd' volume:
SAMPLE_VOLUME_SIZE      = 0x6FFE00
SAMPLE_VOLUME_NAME      = 'NTFS Volume'
SAMPLE_VOLUME_SERIAL    = 0xb2e44491c5000000L
SAMPLE_VOLUME_CHECKSUM  = 0x1ae444
SAMPLE_MFT_ZONE_SIZE    = 0xDF000
SAMPLE_BYTES_PER_SECTOR = 512

class TestNtfsPlugin(unittest.TestCase):
    def setUp(self):
        self.filename = 'sample_images/ntfs_mbr.vhd'
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
        # remove plugin registration
        self.detector._clear_plugins()


class TestBpb(unittest.TestCase):
    def test_init(self):
        bpb = Bpb(
            filename='sample_images/ntfs_bootsector.bin',
            offset=BPB_OFFSET
        )

        self.assertEquals(bpb.bytes_per_sector, SAMPLE_BYTES_PER_SECTOR)
        self.assertEquals(bpb.sectors_per_cluster, 8)
        self.assertEquals(bpb.reserved_sectors, 0)
        self.assertEquals(bpb.media_descriptor, 0xF8)
        self.assertEquals(bpb.sectors_per_track, 0x3F)
        self.assertEquals(bpb.number_of_heads, 0xFF)
        self.assertEquals(bpb.total_sectors, 0x37FF)
        self.assertEquals(bpb.mft_cluster, 0x255)
        self.assertEquals(bpb.mft_mirror_cluster, 0x2)
        self.assertEquals(bpb.clusters_per_mft, -10)
        self.assertEquals(bpb.clusters_per_index, 0x1)
        self.assertEquals(bpb.volume_serial, SAMPLE_VOLUME_SERIAL)
        self.assertEquals(bpb.checksum, SAMPLE_VOLUME_CHECKSUM)
        self.assertEquals(bpb.mft_offset, 0x255000)
        self.assertEquals(bpb.mft_mirror_offset, 0x2000)
        self.assertEquals(bpb.mft_record_size, 1024)


class TestBootsector(unittest.TestCase):
    def test_init(self):
        bootsector = BootSector(filename='sample_images/ntfs_bootsector.bin')
        self.assertEquals(bootsector.oem_id, 'NTFS    ')


class TestNtfsVolume(unittest.TestCase):
    def test_load(self):
        offset = 0x10000
        filename = 'sample_images/ntfs_mbr.vhd'
        ntfs_vol = NtfsVolume()
        ntfs_vol.load(filename=filename, offset=offset)
        self.assertEquals(ntfs_vol.offset, offset)
        self.assertEquals(ntfs_vol.filename, filename)
        self.assertEquals(
            len(ntfs_vol.mft_table._entries), NUM_SYSTEM_ENTRIES)
        self.assertEquals(ntfs_vol.major_ver, 3)
        self.assertEquals(ntfs_vol.minor_ver, 1)
        self.assertEquals(ntfs_vol.vol_name, SAMPLE_VOLUME_NAME)
        self.assertEquals(ntfs_vol.size, SAMPLE_VOLUME_SIZE)
        self.assertEquals(ntfs_vol.mft_table_offset, offset + \
        ntfs_vol.bootsector.bpb.mft_offset)
        self.assertEquals(ntfs_vol.mft_mirror_offset, offset + \
        ntfs_vol.bootsector.bpb.mft_mirror_offset)
        self.assertEquals(ntfs_vol.mft_zone_size, SAMPLE_MFT_ZONE_SIZE)


class TestMftTable(unittest.TestCase):
    def test_init(self):
        mft = MftTable(
            filename='sample_images/ntfs_mft_table.bin',
        )

        self.assertEquals(len(mft._entries), 0)
        entry = mft.get_entry(0)
        self.assertTrue(entry is not None)
        self.assertEquals(len(mft._entries), 1)

    def test_get_entry(self):
        mft = MftTable(
            filename='sample_images/ntfs_mft_table.bin',
        )

        self.assertTrue(mft.get_entry(0) is not None)
        self.assertEquals(len(mft._entries), 1)
        self.assertTrue(mft.get_entry(3) is not None)
        self.assertTrue(mft.get_entry(2) is not None)
        self.assertEquals(len(mft._entries), 3)
