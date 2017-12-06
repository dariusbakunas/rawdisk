import unittest
from rawdisk.main import parse_args


class TestMain(unittest.TestCase):
    def test_parseargs_verbose_overrides_debug_loglevel(self):
        arguments = parse_args(
            ['--verbose', '-f', 'test.img', '--log-level', 'INFO'])

        self.assertEqual('DEBUG', arguments.log_level)

    def test_parseargs_returns_correct_args(self):
        arguments = parse_args(
            ['-f', 'test.img', '--log-level',
             'ERROR', '--log-config', 'log.yaml']
        )

        self.assertEqual('test.img', arguments.filename)
        self.assertEqual('ERROR', arguments.log_level)
        self.assertEqual('log.yaml', arguments.log_config)
