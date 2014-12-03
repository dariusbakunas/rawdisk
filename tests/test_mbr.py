import unittest
import mock
from rawdisk.scheme.mbr import Mbr
from rawdisk.scheme.mbr import PT_TABLE_SIZE


class TestMbrModule(unittest.TestCase):
    def setUp(self):
        self.mbr = Mbr(
            filename='sample_images/ntfs_mbr.vhd',
        )

    def test_partition_table_has_correct_size(self):
        self.assertEquals(self.mbr.partition_table.size, PT_TABLE_SIZE)

    def test_partition_table_has_one_entry(self):
        self.assertEquals(len(self.mbr.partition_table.entries), 1)

    def test_partition_entry(self):
        part = self.mbr.partition_table.entries[0]

        self.assertEquals(part.fields.boot_indicator, 0)
        self.assertEquals(part.fields.starting_head, 2)
        self.assertEquals(part.fields.starting_sector, 3)
        self.assertEquals(part.fields.starting_cylinder, 0)
        self.assertEquals(part.fields.part_type, 7)
        self.assertEquals(part.fields.ending_head, 229)
        self.assertEquals(part.fields.ending_sector, 37)
        self.assertEquals(part.fields.ending_cylinder, 0)
        self.assertEquals(part.fields.relative_sector, 128)
        self.assertEquals(part.fields.total_sectors, 14336)
        self.assertEquals(part.part_offset, 65536)

    @mock.patch('rawdisk.scheme.mbr.Mbr.get_ushort_le')
    def test_init_invalid_signature_throws_exception(self, mock_get_ushort):
        mock_get_ushort.return_value = 0xBBBB
        with self.assertRaises(Exception):
            Mbr(
                filename='sample_images/ntfs_mbr.vhd',
            )
