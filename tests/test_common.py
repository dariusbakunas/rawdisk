import unittest
from rawdisk.scheme.common import detect_scheme, \
    SCHEME_MBR, SCHEME_GPT, SCHEME_UNKNOWN


class TestCommon(unittest.TestCase):
    def test_detect_mbr_scheme(self):
        scheme = detect_scheme('sample_images/ntfs_mbr.vhd')
        self.assertEqual(SCHEME_MBR, scheme)

    def test_detect_gpt_scheme(self):
        scheme = detect_scheme('sample_images/ntfs_primary_gpt.bin')
        self.assertEqual(SCHEME_GPT, scheme)

    def test_detect_unknown_scheme(self):
        scheme = detect_scheme('sample_images/ntfs_mft_table.bin')
        self.assertEqual(SCHEME_UNKNOWN, scheme)
