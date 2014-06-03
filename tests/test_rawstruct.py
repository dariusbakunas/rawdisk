import unittest
import mock
from rawdisk.util.rawstruct import RawStruct


class TestRawStruct(unittest.TestCase):
    def setUp(self):
        self.sample_data = b'\xa1\xb1\xc1\xd1\xe1\xf1'

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
