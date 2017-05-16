import cmd, sys
import logging
from rawdisk.reader import Reader
from rawdisk.modes.mode import Mode

class CliMode(Mode):
    @staticmethod
    def entry(args=None):
        cli = CliShell()
        cli.initialize()
        cli.cmdloop()

class CliShell(cmd.Cmd):
    intro = 'Welcome to rawdisk shell. Type help or ? to list command.\n'
    prompt = 'rawdisk > '

    def do_quit(self, arg):
        self.close()
        return True

    def close(self):
        return
