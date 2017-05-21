#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from rawdisk.util.filetimes import dt_to_filetime, filetime_to_dt, UTC, ZERO
from datetime import datetime


class TestFiletimesModule(unittest.TestCase):
    def test_dt_to_filetime(self):
        value = datetime(2009, 7, 25, 23, 0)
        self.assertEqual(128930364000000000, dt_to_filetime(value))

    def test_filetime_to_dt(self):
        value = 116444736000000000
        self.assertEqual(datetime(1970, 1, 1, 0, 0), filetime_to_dt(value))

    def test_utc(self):
        utc = UTC()

        self.assertEqual(utc.tzname(None), "UTC")
        self.assertEqual(utc.utcoffset(None), ZERO)


if __name__ == "__main__":
    unittest.main()
