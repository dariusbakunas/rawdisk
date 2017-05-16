import cmd, sys
from ..mode import Mode

class CliMode(Mode):
    @staticmethod
    def entry():
        CliShell().cmdloop()

class CliShell(cmd.Cmd):
    intro = 'Welcome to rawdisk shell. Type help or ? to list command.\n'
    prompt = 'rawdisk > '

    def do_quit(self, arg):
        self.close()
        return True

    def close(self):
        return
