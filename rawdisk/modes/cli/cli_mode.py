import cmd, sys
import logging
import numpy as np
from rawdisk.reader import Reader
from rawdisk.modes.mode import Mode
from tabulate import tabulate


class CliMode(Mode):
    @staticmethod
    def entry(args=None):
        cli = CliShell()
        cli.initialize()
        cli.cmdloop()

class CliShell(cmd.Cmd):
    def __init__(self, completekey='tab', stdin=None, stdout=None):
        super().__init__(completekey, stdin, stdout)
        self.prompt = self.get_prompt()
        self.ruler = '-'
        self.intro = 'Welcome to rawdisk shell. Type help or ? to list command.\n'
        self.reader = Reader()
        self.logger = logging.getLogger(__name__)

    def initialize(self):
        self.reader.load_plugins()

    def do_plugins(self, arg):
        """List loaded plugins"""
        plugins = self.reader.manager.fs_plugins

        data = [[plugin.name, plugin.author, plugin.version, plugin.description] for plugin in plugins]
        table = tabulate(tabular_data=data, headers=['NAME', 'AUTHOR', 'VERSION', 'DESCRIPTION'])

        print(table)

    def do_quit(self, arg):
        """Exit CLI"""
        self.close()
        return True

    def do_exit(self, arg):
        """Exit CLI"""
        self.close()
        return True

    def get_prompt(self):
        return 'rawdisk > '

    def close(self):
        return

if __name__ == '__main__':
    CliMode.entry()
