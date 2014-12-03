# -*- coding: utf-8 -*-

import unittest
from rawdisk.scheme.gpt import Gpt, GptPartitionEntry
from uuid import UUID


class TestGptModule(unittest.TestCase):
    def setUp(self):
        self.gpt = Gpt()

    def test_load(self):
        self.gpt.load(
            filename='sample_images/ntfs_primary_gpt.bin',
            bs=512
        )

        header = self.gpt.header
        self.assertEquals(header.fields.signature, 'EFI PART')
        self.assertEquals(header.fields.revision, 0x10000)
        self.assertEquals(header.fields.header_size, 92)
        self.assertEquals(header.fields.crc32, 0x58c12499)
        self.assertEquals(header.fields.current_lba, 1)
        self.assertEquals(header.fields.backup_lba, 262143)
        self.assertEquals(header.fields.first_usable_lba, 34)
        self.assertEquals(header.fields.last_usable_lba, 262110)
        self.assertEquals(
            UUID(bytes_le = "".join(map(chr, header.fields.disk_guid))),
            UUID('af9966e5-00fb-45cd-be63-262d9188dce7')
        )
        self.assertEquals(header.fields.part_lba, 2)
        self.assertEquals(header.fields.num_partitions, 128)
        self.assertEquals(header.fields.part_size, 128)
        self.assertEquals(header.fields.part_array_crc32, 0xf0f45a62)
        self.assertEquals(len(self.gpt.partition_entries), 2)


class TestGptPartitionEntry(unittest.TestCase):
    def setUp(self):
        with open('sample_images/gpt_partition_entry.bin', 'rb') as f:
            self.data = f.read()

    def test_init(self):
        part = GptPartitionEntry(self.data)
        self.assertEquals(
            part.type_guid,
            UUID('ebd0a0a2-b9e5-4433-87c0-68b6b72699c7')    # NTFS guid
        )
        self.assertEquals(
            part.part_guid,
            UUID('5cc56719-2e2b-4a46-b455-c5c26e74675c')
        )
        self.assertEquals(part.first_lba, 65664)
        self.assertEquals(part.last_lba, 258175)
        self.assertEquals(part.attr_flags, 0)
        self.assertEquals(part.name, 'Basic data partition')
