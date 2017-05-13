#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import uuid
from rawdisk.plugins.filesystems.ntfs.ntfs import NtfsPlugin
from rawdisk.plugins.filesystems.ntfs.bootsector import BootSector
from rawdisk.plugins.filesystems.ntfs.mft import MftTable
from rawdisk.plugins.filesystems.ntfs.ntfs_volume import NtfsVolume, \
    NUM_SYSTEM_ENTRIES
from rawdisk.filesystems.detector import FilesystemDetector

# These are real values for the sample 'ntfs_mbr.vhd' volume:
SAMPLE_OEM_ID = b'NTFS    '
SAMPLE_NTFS_PART_OFFSET = 0x10000
SAMPLE_TOTAL_SECTORS = 0x37FF
SAMPLE_NUM_HEADS = 0xFF
SAMPLE_CLUSTERS_PER_INDEX = 0x1
SAMPLE_SECTORS_PER_TRACK = 0x3F
SAMPLE_SECTORS_PER_CLUSTER = 8
SAMPLE_VOLUME_HIDDEN_SECTORS = 128
SAMPLE_CLUSTERS_PER_MFT = -10
SAMPLE_MEDIA_DESCRIPTOR = 0xF8
SAMPLE_RESERVED_SECTORS = 0
SAMPLE_VOLUME_SIZE = 0x6FFE00
SAMPLE_VOLUME_NAME = 'NTFS Volume'
SAMPLE_VOLUME_SERIAL = 0x1AE444B2E44491C5
SAMPLE_VOLUME_MAJOR_VER = 3
SAMPLE_VOLUME_MINOR_VER = 1
SAMPLE_MFT_CLUSTER = 0x255
SAMPLE_MFT_MIRR_CLUSTER = 0x2
SAMPLE_MFT_OFFSET = 0x255000
SAMPLE_MFT_MIRR_OFFSET = 0x2000
SAMPLE_MFT_RECORD_SIZE = 1024
SAMPLE_MFT_ZONE_SIZE = 0xDF000
SAMPLE_BYTES_PER_SECTOR = 512


class TestNtfsPlugin(unittest.TestCase):
    def setUp(self):
        self.filename = 'sample_images/ntfs_mbr.vhd'
        self.offset = SAMPLE_NTFS_PART_OFFSET
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

        self.assertEqual(len(mbr_plugins), 1)
        self.assertEqual(len(gpt_plugins), 1)

    def tearDown(self):
        # remove plugin registration
        self.detector._clear_plugins()


class TestBootsector(unittest.TestCase):
    def test_init(self):
        bootsector = BootSector(filename='sample_images/ntfs_bootsector.bin')
        self.assertEqual(bootsector.oem_id, SAMPLE_OEM_ID)
        self.assertEqual(
            bootsector.bpb.bytes_per_sector, SAMPLE_BYTES_PER_SECTOR)
        self.assertEqual(
            bootsector.bpb.sectors_per_cluster, SAMPLE_SECTORS_PER_CLUSTER)
        self.assertEqual(
            bootsector.bpb.reserved_sectors, SAMPLE_RESERVED_SECTORS)
        self.assertEqual(bootsector.bpb.media_type, SAMPLE_MEDIA_DESCRIPTOR)
        self.assertEqual(
            bootsector.bpb.sectors_per_track, SAMPLE_SECTORS_PER_TRACK)
        self.assertEqual(bootsector.bpb.heads, SAMPLE_NUM_HEADS)
        self.assertEqual(
            bootsector.bpb.hidden_sectors, SAMPLE_VOLUME_HIDDEN_SECTORS)
        self.assertEqual(bootsector.bpb.total_sectors, SAMPLE_TOTAL_SECTORS)
        self.assertEqual(
            bootsector.extended_bpb.mft_cluster, SAMPLE_MFT_CLUSTER)
        self.assertEqual(
            bootsector.extended_bpb.mft_mirror_cluster,
            SAMPLE_MFT_MIRR_CLUSTER
            )
        self.assertEqual(
            bootsector.extended_bpb.clusters_per_mft, SAMPLE_CLUSTERS_PER_MFT)
        self.assertEqual(
            bootsector.extended_bpb.clusters_per_index,
            SAMPLE_CLUSTERS_PER_INDEX
            )
        self.assertEqual(
            bootsector.extended_bpb.volume_serial, SAMPLE_VOLUME_SERIAL)
        self.assertEqual(bootsector.mft_offset, SAMPLE_MFT_OFFSET)
        self.assertEqual(bootsector.mft_mirror_offset, SAMPLE_MFT_MIRR_OFFSET)
        self.assertEqual(bootsector.mft_record_size, SAMPLE_MFT_RECORD_SIZE)


class TestNtfsVolume(unittest.TestCase):
    def test_load(self):
        offset = SAMPLE_NTFS_PART_OFFSET
        filename = 'sample_images/ntfs_mbr.vhd'
        ntfs_vol = NtfsVolume()
        ntfs_vol.load(filename=filename, offset=offset)
        self.assertEqual(ntfs_vol.offset, offset)
        self.assertEqual(ntfs_vol.filename, filename)
        self.assertEqual(
            len(ntfs_vol.mft_table._entries), NUM_SYSTEM_ENTRIES)
        self.assertEqual(ntfs_vol.major_ver, SAMPLE_VOLUME_MAJOR_VER)
        self.assertEqual(ntfs_vol.minor_ver, SAMPLE_VOLUME_MINOR_VER)
        self.assertEqual(ntfs_vol.vol_name, SAMPLE_VOLUME_NAME)
        self.assertEqual(ntfs_vol.size, SAMPLE_VOLUME_SIZE)
        self.assertEqual(
            ntfs_vol.mft_table_offset, offset +
            ntfs_vol.bootsector.mft_offset)
        self.assertEqual(
            ntfs_vol.mft_mirror_offset, offset +
            ntfs_vol.bootsector.mft_mirror_offset)
        self.assertEqual(ntfs_vol.mft_zone_size, SAMPLE_MFT_ZONE_SIZE)


class TestMftTable(unittest.TestCase):
    def test_init(self):
        mft = MftTable(
            filename='sample_images/ntfs_mft_table.bin',
        )

        self.assertEqual(len(mft._entries), 0)
        entry = mft.get_entry(0)
        self.assertTrue(entry is not None)
        self.assertEqual(len(mft._entries), 1)

    def test_get_entry(self):
        mft = MftTable(
            filename='sample_images/ntfs_mft_table.bin',
        )

        self.assertTrue(mft.get_entry(0) is not None)
        self.assertEqual(len(mft._entries), 1)
        self.assertTrue(mft.get_entry(3) is not None)
        self.assertTrue(mft.get_entry(2) is not None)
        self.assertEqual(len(mft._entries), 3)


class TestMftEntry(unittest.TestCase):
    def test_init(self):
        mft = MftTable(
            filename='sample_images/ntfs_mft_table.bin',
        )
        entry = mft.get_entry(0)

        header = entry.header
        self.assertEqual(header.signature, b'FILE')
        self.assertEqual(header.upd_seq_array_offset, 0x30)
        self.assertEqual(header.upd_seq_array_size, 0x3)
        self.assertEqual(header.logfile_seq_number, 0x104D82)
        self.assertEqual(header.seq_number, 0x1)
        self.assertEqual(header.hard_link_count, 0x1)
        self.assertEqual(header.first_attr_offset, 0x38)
        self.assertEqual(header.flags, 0x1)
        self.assertEqual(header.used_size, 0x1A0)
        self.assertEqual(header.allocated_size, 0x400)
        self.assertEqual(header.base_file_record, 0x0)
        self.assertEqual(header.next_attr_id, 0x0)
        self.assertEqual(header.mft_record_number, 0x0)

        self.assertEqual(len(entry.attributes), 4)
        self.assertEqual(entry.fname_str, '$MFT')
        self.assertEqual(entry.name_str, 'Master File Table')
        self.assertFalse(entry.is_directory)
        self.assertTrue(entry.is_file)
        self.assertTrue(entry.is_in_use)
        self.assertTrue(entry.lookup_attribute(0x10) is not None)
