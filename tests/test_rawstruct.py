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
import mock
import struct
import uuid
from rawdisk.util.rawstruct import RawStruct


class TestRawStruct(unittest.TestCase):
    def setUp(self):
        self.sample_data = b'\xa1\xb1\xc1\xd1\xe1\xf1\xb1\xa1\xc1'
        self.sample_uuid_data = b'\x12\x34\x56\x78'*4

    def test_init_from_data(self):
        r = RawStruct(data=self.sample_data)
        self.assertEqual(
            (r.size, r.data), (len(self.sample_data), self.sample_data))

    def test_init_from_data_with_offset(self):
        offset = 2
        length = 3
        r1 = RawStruct(data=self.sample_data, offset=offset)
        r2 = RawStruct(data=self.sample_data, offset=offset, length=length)
        self.assertEqual(
            (r1.size, r1.data),
            (len(self.sample_data) - offset, self.sample_data[offset:])
        )

        self.assertEqual(
            (r2.size, r2.data),
            (length, self.sample_data[offset:offset + length])
        )

    def test_init_with_filename(self):
        offset = 2
        length = 3
        file_mock = mock.MagicMock()
        with mock.patch('__builtin__.open', file_mock):
            manager = file_mock.return_value.__enter__.return_value
            manager.read.side_effect = \
                lambda length: self.sample_data[offset:offset+length]
            r = RawStruct(filename='test', offset=offset, length=length)

            self.assertEqual(
                (r.size, r.data),
                (length, self.sample_data[offset:offset + length])
            )

    def test_get_uchar(self):
        offset = 2
        r = RawStruct(data=self.sample_data)
        self.assertEqual(
            r.get_uchar(offset),
            struct.unpack("B", self.sample_data[offset:offset+1])[0])

    def test_get_ushort_le(self):
        offset = 0
        r = RawStruct(data=self.sample_data)
        self.assertEqual(
            r.get_ushort_le(offset),
            struct.unpack("<H", self.sample_data[offset:offset+2])[0])

    def test_get_ushort_be(self):
        offset = 2
        r = RawStruct(data=self.sample_data)
        self.assertEqual(
            r.get_ushort_be(offset),
            struct.unpack(">H", self.sample_data[offset:offset+2])[0])

    def test_get_uint_le(self):
        offset = 0
        r = RawStruct(data=self.sample_data)
        self.assertEqual(
            r.get_uint_le(offset),
            struct.unpack("<I", self.sample_data[offset:offset+4])[0])

    def test_get_uint_be(self):
        offset = 0
        r = RawStruct(data=self.sample_data)
        self.assertEqual(
            r.get_uint_be(offset),
            struct.unpack(">I", self.sample_data[offset:offset+4])[0])

    def test_get_ulong_le(self):
        offset = 0
        r = RawStruct(data=self.sample_data)
        self.assertEqual(
            r.get_ulong_le(offset),
            struct.unpack("<L", self.sample_data[offset:offset+4])[0])

    def test_get_ulong_be(self):
        offset = 0
        r = RawStruct(data=self.sample_data)
        self.assertEqual(
            r.get_ulong_be(offset),
            struct.unpack(">L", self.sample_data[offset:offset+4])[0])

    def test_get_ulonglong_le(self):
        offset = 0
        r = RawStruct(data=self.sample_data)
        self.assertEqual(
            r.get_ulonglong_le(offset),
            struct.unpack("<Q", self.sample_data[offset:offset+8])[0])

    def test_get_ulonglong_be(self):
        offset = 0
        r = RawStruct(data=self.sample_data)
        self.assertEqual(
            r.get_ulonglong_be(offset),
            struct.unpack(">Q", self.sample_data[offset:offset+8])[0])

    def test_get_uuid_le(self):
        r = RawStruct(data=self.sample_uuid_data)
        self.assertEqual(
            r.get_uuid_le(0),
            uuid.UUID(bytes_le=self.sample_uuid_data))

    def test_get_uuid_be(self):
        r = RawStruct(data=self.sample_uuid_data)
        self.assertEqual(
            r.get_uuid_be(0),
            uuid.UUID(bytes=self.sample_uuid_data))
