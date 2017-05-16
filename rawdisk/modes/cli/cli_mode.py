import cmd, sys
import logging
import numpy as np
from rawdisk.reader import Reader
from rawdisk.modes.mode import Mode
from rawdisk.util.output import format_table

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
        plugins = self.reader.manager.fs_plugins

        rows = format_table(
            headers=['NAME', 'AUTHOR', 'VERSION'],
            columns=['name', 'author', 'version'],
            values=plugins
        )

        print('\n'.join(rows))

    def do_quit(self, arg):
        """Exit CLI"""
        self.close()
        return True

    def do_exit(self, arg):
        """Exit CLI"""
        self.close()
        return True

    def do_log(self, message):
        self.logger.info(message)

    def get_prompt(self):
        return 'rawdisk > '

    def close(self):
        return

if __name__ == '__main__':
    CliMode.entry()
