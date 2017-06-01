import unittest
import xml.etree.ElementTree as xml
from rawdisk.exporting.xml_exporter import XmlExporter
from rawdisk.scheme.mbr import Mbr
from rawdisk.scheme.gpt import Gpt
from rawdisk.util.xml import prettify


class XmlExporterTest(unittest.TestCase):
    def setUp(self):
        self.exporter = XmlExporter

    def test_export_partition_table(self):
        gpt = Gpt()
        gpt.load(filename='sample_images/ntfs_primary_gpt.bin')
        root = self.exporter.get_partitioning_scheme_xml(scheme=gpt)
        output = prettify(root)
        expected = ''
        self.assertMultiLineEqual(output, expected)
