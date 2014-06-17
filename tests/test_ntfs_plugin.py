# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2014 Darius Bakunas

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import unittest
import uuid
from rawdisk.plugins.filesystems.ntfs.ntfs import NtfsPlugin
from rawdisk.plugins.filesystems.ntfs.bpb import Bpb, BPB_OFFSET
from rawdisk.plugins.filesystems.ntfs.bootsector import BootSector
from rawdisk.plugins.filesystems.ntfs.mft import MftTable
from rawdisk.plugins.filesystems.ntfs.ntfs_volume import NtfsVolume, \
    NUM_SYSTEM_ENTRIES
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
        # remove plugin registration
        self.detector._clear_plugins()


class TestBpb(unittest.TestCase):
    def test_init(self):
        bpb = Bpb(
            filename='sample_images/ntfs_bootsector.bin',
            offset=BPB_OFFSET
        )

        self.assertEquals(bpb.bytes_per_sector, 512)
        self.assertEquals(bpb.sectors_per_cluster, 8)
        self.assertEquals(bpb.reserved_sectors, 0)
        self.assertEquals(bpb.media_descriptor, 0xF8)
        self.assertEquals(bpb.sectors_per_track, 0x3F)
        self.assertEquals(bpb.number_of_heads, 0xFF)
        self.assertEquals(bpb.total_sectors, 0x1FE7FF)
        self.assertEquals(bpb.mft_cluster, 0x15455)
        self.assertEquals(bpb.mft_mirror_cluster, 0x2)
        self.assertEquals(bpb.clusters_per_mft, -10)
        self.assertEquals(bpb.clusters_per_index, 0x1)
        self.assertEquals(bpb.volume_serial, 0xa028d573cf000000L)
        self.assertEquals(bpb.checksum, 0xE228D5)
        self.assertEquals(bpb.mft_offset, 0x15455000)
        self.assertEquals(bpb.mft_mirror_offset, 0x2000)
        self.assertEquals(bpb.mft_record_size, 1024)


class TestBootsector(unittest.TestCase):
    def test_init(self):
        bootsector = BootSector(filename='sample_images/ntfs_bootsector.bin')
        self.assertEquals(bootsector.oem_id, 'NTFS    ')


class TestNtfsVolume(unittest.TestCase):
    def test_load(self):
        offset = 0x10000
        filename = 'sample_images/ntfs.vhd'
        ntfs_vol = NtfsVolume()
        ntfs_vol.load(filename=filename, offset=offset)
        self.assertEquals(ntfs_vol.offset, offset)
        self.assertEquals(ntfs_vol.filename, filename)
        self.assertEquals(len(ntfs_vol.mft_table._entries), NUM_SYSTEM_ENTRIES)
        self.assertEquals(ntfs_vol.major_ver, 3)
        self.assertEquals(ntfs_vol.minor_ver, 1)
        self.assertEquals(ntfs_vol.vol_name, u'New Volume')
        self.assertEquals(ntfs_vol.size, 0x3fcffe00)
        self.assertEquals(ntfs_vol.mft_table_offset, offset + \
            ntfs_vol.bootsector.bpb.mft_offset)
        self.assertEquals(ntfs_vol.mft_mirror_offset, offset + \
            ntfs_vol.bootsector.bpb.mft_mirror_offset)
        self.assertEquals(ntfs_vol.mft_zone_size, 0x7f9f000)


class TestMftTable(unittest.TestCase):
    def test_init(self):
        mft = MftTable(
            filename='sample_images/ntfs_mft_table.bin',
        )

        self.assertEquals(len(mft._entries), 0)
        entry = mft.get_entry(0)
        self.assertIsNotNone(entry)
        self.assertEquals(len(mft._entries), 1)

    def test_get_entry(self):
        mft = MftTable(
            filename='sample_images/ntfs_mft_table.bin',
        )

        self.assertIsNotNone(mft.get_entry(0))
        self.assertEquals(len(mft._entries), 1)
        self.assertIsNotNone(mft.get_entry(3))
        self.assertIsNotNone(mft.get_entry(2))
        self.assertEquals(len(mft._entries), 3)

class TestMftEntryHeader(unittest.TestCase):
    def test_init(self):
        mft = MftTable(
            filename='sample_images/ntfs_mft_table.bin',
        )
        entry = mft.get_entry(0)
        header = entry.header
        self.assertEquals(header.file_signature, 'FILE')
        self.assertEquals(header.update_seq_array_offset, 0x30)
        self.assertEquals(header.update_seq_array_size, 0x3)
        self.assertEquals(header.logfile_seq_number, 0x2022ea)
        self.assertEquals(header.seq_number, 0x1)
        self.assertEquals(header.hard_link_count, 0x1)
        self.assertEquals(header.first_attr_offset, 0x38)
        self.assertEquals(header.flags, 0x1)
        self.assertEquals(header.used_size, 0x1A0)
        self.assertEquals(header.allocated_size, 0x400)
        self.assertEquals(header.base_file_record, 0x0)
        self.assertEquals(header.next_attr_id, 0x0)
        self.assertEquals(header.mft_record_number, 0x0)

class TestMftEntry(unittest.TestCase):
    def test_init(self):
        mft = MftTable(
            filename='sample_images/ntfs_mft_table.bin',
        )

        entry = mft.get_entry(0)
        self.assertEquals(len(entry.attributes), 4)
        self.assertEquals(entry.fname_str, '$MFT')
        self.assertEquals(entry.name_str, 'Master File Table')
        self.assertFalse(entry.is_directory)
        self.assertTrue(entry.is_file)
        self.assertTrue(entry.is_in_use)
        self.assertIsNotNone(entry.lookup_attribute(0x10))


class TestMftAttrHeader(unittest.TestCase):
    def test_init(self):
        mft = MftTable(
            filename='sample_images/ntfs_mft_table.bin',
        )

        entry = mft.get_entry(0)
        attr = entry.lookup_attributef

