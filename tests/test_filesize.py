#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from rawdisk.util.filesize import size_str


class TestFilesizeModule(unittest.TestCase):
    def test_size_str(self):
        self.assertEqual(size_str(1024), "1.00KB")

    def test_size_str_w_format(self):
        self.assertEqual(size_str(100000, "{0:E}"), "1.000000E+05")


if __name__ == "__main__":
    unittest.main()
