import unittest
from rawdisk.scheme.common import detect_scheme, PartitionScheme


class TestCommon(unittest.TestCase):
    def test_detect_mbr_scheme(self):
        scheme = detect_scheme('sample_images/ntfs_mbr.vhd')
        self.assertEqual(PartitionScheme.SCHEME_MBR, scheme)

    def test_detect_gpt_scheme(self):
        scheme = detect_scheme('sample_images/ntfs_primary_gpt.bin')
        self.assertEqual(PartitionScheme.SCHEME_GPT, scheme)

    def test_detect_unknown_scheme(self):
        scheme = detect_scheme('sample_images/ntfs_mft_table.bin')
        self.assertEqual(PartitionScheme.SCHEME_UNKNOWN, scheme)
