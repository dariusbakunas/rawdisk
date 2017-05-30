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
        self.assertEqual(header.signature, b'EFI PART')
        self.assertEqual(header.revision, 0x10000)
        self.assertEqual(header.header_size, 92)
        self.assertEqual(header.crc32, 0x58c12499)
        self.assertEqual(header.current_lba, 1)
        self.assertEqual(header.backup_lba, 262143)
        self.assertEqual(header.first_usable_lba, 34)
        self.assertEqual(header.last_usable_lba, 262110)
        self.assertEqual(
            UUID(bytes_le=bytes(header.disk_guid)),
            UUID('af9966e5-00fb-45cd-be63-262d9188dce7')
        )
        self.assertEqual(header.part_lba, 2)
        self.assertEqual(header.num_partitions, 128)
        self.assertEqual(header.part_size, 128)
        self.assertEqual(header.part_array_crc32, 0xf0f45a62)
        self.assertEqual(len(self.gpt.partition_entries), 2)


class TestGptPartitionEntry(unittest.TestCase):
    def setUp(self):
        with open('sample_images/gpt_partition_entry.bin', 'rb') as f:
            self.data = f.read()

    def test_init(self):
        part = GptPartitionEntry(self.data)
        self.assertEqual(
            part.type_guid,
            UUID('ebd0a0a2-b9e5-4433-87c0-68b6b72699c7')    # NTFS guid
        )
        self.assertEqual(
            part.part_guid,
            UUID('5cc56719-2e2b-4a46-b455-c5c26e74675c')
        )
        self.assertEqual(part.fields.first_lba, 65664)
        self.assertEqual(part.fields.last_lba, 258175)
        self.assertEqual(part.fields.attr_flags, 0)
        self.assertEqual(part.fields.name, 'Basic data partition')
