import unittest
from unittest.mock import Mock

from rawdisk.ui.cli.cli_mode import CliMode, CliShell


class CliModeTest(unittest.TestCase):
    def test_initialize_loads_fs_plugins(self):
        session = Mock()
        cli = CliShell(session=session)
        cli.initialize()
        session.load_plugins.assert_called_once_with()
