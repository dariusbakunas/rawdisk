import unittest
import hashlib
import os
import tempfile
from rawdisk.exporting.binary_exporter import BinaryExporter


TEST_MD5 = '30c142304ddc91f8a7ac0a8b409e5817'

class BinaryExporterTest(unittest.TestCase):
    def setUp(self):
        self.exporter = BinaryExporter()

    def md5(self, filename):
        hash_md5 = hashlib.md5()
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def test_ntfs_boot_sector_export(self):
        output = os.path.join(tempfile.gettempdir(), 'test.bin')

        self.exporter.export(
            input_filename='sample_images/ntfs_mbr.vhd',
            output_filename=output,
            start_offset=0x10000,
            size=512
        )

        md5hash = self.md5(output)
        self.assertEqual(TEST_MD5, md5hash)
        os.remove(output)
