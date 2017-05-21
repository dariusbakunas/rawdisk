#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import uuid
from rawdisk.filesystems.detector import FilesystemDetector
from mock import Mock, PropertyMock


class TestFilesystemDetector(unittest.TestCase):
    def setUp(self):
        self.guid_fs_id = uuid.UUID('{EBD0A0A2-B9E5-4433-87C0-68B6B72699C7}')
        self.mbr_fs_id = 0x07

    def test_multiple_mbr_plugins_for_same_id(self):
        detector = FilesystemDetector()
        detector.register_mbr_plugin(self.mbr_fs_id, object())
        detector.register_mbr_plugin(self.mbr_fs_id, object())

        self.assertEqual(len(detector.get_mbr_plugins(fs_id=self.mbr_fs_id)), 2)

    def test_multiple_gpt_plugins_for_same_id(self):
        detector = FilesystemDetector()
        detector.register_gpt_plugin(self.guid_fs_id, object())
        detector.register_gpt_plugin(self.guid_fs_id, object())

        self.assertEqual(len(detector.get_gpt_plugins(fs_guid=self.guid_fs_id)), 2)

    def test_detection_with_no_plugins(self):
        detector = FilesystemDetector()
        self.assertIsNone(detector.detect_mbr("filename", 0, self.mbr_fs_id))
        self.assertIsNone(detector.detect_gpt("filename", 0, self.guid_fs_id))

    def test_init_with_plugin_list_registers_plugins(self):
        mbr_plugin_mock = Mock()
        mbr_plugin_mock.mbr_identifiers = [self.mbr_fs_id]
        mbr_plugin_mock.gpt_identifiers = []


        gpt_plugin_mock = Mock()
        gpt_plugin_mock.mbr_identifiers = []
        gpt_plugin_mock.gpt_identifiers = [self.guid_fs_id]

        detector = FilesystemDetector(fs_plugins=[mbr_plugin_mock, gpt_plugin_mock])

        detector.detect_mbr(filename="filename", offset=0x10, fs_id=self.mbr_fs_id)
        mbr_plugin_mock.detect.assert_called_once_with("filename", 0x10)

        detector.detect_gpt(filename="filename", offset=0x20, fs_guid=self.guid_fs_id)
        gpt_plugin_mock.detect.assert_called_once_with("filename", 0x20)

    def test_detect_mbr_calls_detect_on_mbr_plugin(self):
        filename = "filename"
        offset = 0x10
        detector = FilesystemDetector()
        mbr_plugin_mock = Mock()
        mbr_plugin_mock.get_volume_object.return_value = "volume"
        detector.register_mbr_plugin(self.mbr_fs_id, mbr_plugin_mock)
        detector.detect_mbr(filename, offset, self.mbr_fs_id)

        mbr_plugin_mock.detect.assert_called_once_with(filename, offset)

    def test_detect_mbr_returns_valid_volume_object(self):
        detector = FilesystemDetector()
        mbr_plugin_mock = Mock()
        mbr_plugin_mock.get_volume_object.return_value = "volume"
        mbr_plugin_mock.detect.return_value = True
        detector.register_mbr_plugin(self.mbr_fs_id, mbr_plugin_mock)
        volume_object = detector.detect_mbr("filename", 0, self.mbr_fs_id)
        self.assertEqual(volume_object, "volume")

    def test_detect_mbr_returns_none_when_plugin_returns_false(self):
        detector = FilesystemDetector()
        mbr_plugin_mock = Mock()
        mbr_plugin_mock.get_volume_object.return_value = "volume"
        mbr_plugin_mock.detect.return_value = False
        detector.register_mbr_plugin(self.mbr_fs_id, mbr_plugin_mock)
        volume_object = detector.detect_mbr("filename", 0, self.mbr_fs_id)
        self.assertIsNone(volume_object)

    def test_detect_gpt_calls_detect_on_gpt_plugin(self):
        offset = 0x10
        filename = "filename"
        detector = FilesystemDetector()
        gpt_plugin_mock = Mock()
        gpt_plugin_mock.get_volume_object.return_value = "volume"
        detector.register_gpt_plugin(self.guid_fs_id, gpt_plugin_mock)
        detector.detect_gpt(filename, offset, self.guid_fs_id)

        gpt_plugin_mock.detect.assert_called_once_with(filename, offset)

    def test_detect_gpt_returns_valid_volume_object(self):
        detector = FilesystemDetector()
        gpt_plugin_mock = Mock()
        gpt_plugin_mock.get_volume_object.return_value = "volume"
        gpt_plugin_mock.detect.return_value = True
        detector.register_gpt_plugin(self.guid_fs_id, gpt_plugin_mock)
        volume_object = detector.detect_gpt("filename", 0, self.guid_fs_id)
        self.assertEqual(volume_object, "volume")

    def test_detect_gpt_returns_none_when_plugin_returns_false(self):
        detector = FilesystemDetector()
        gpt_plugin_mock = Mock()
        gpt_plugin_mock.get_volume_object.return_value = "volume"
        gpt_plugin_mock.detect.return_value = False
        detector.register_gpt_plugin(self.guid_fs_id, gpt_plugin_mock)
        volume_object = detector.detect_gpt("filename", 0, self.guid_fs_id)
        self.assertIsNone(volume_object)

    def tearDown(self):
        FilesystemDetector._instances = {}


if __name__ == "__main__":
    unittest.main()
