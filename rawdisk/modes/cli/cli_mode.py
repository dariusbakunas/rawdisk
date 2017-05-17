import logging
import os
from rawdisk.session import Session
from rawdisk.modes.mode import Mode
from tabulate import tabulate
from cmd import Cmd


class CliMode(Mode):
    @staticmethod
    def entry(args=None):
        cli = CliShell()
        cli.initialize()
        cli.cmdloop()


class CliShell(Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = self.get_prompt()
        self.ruler = '-'
        self.intro = 'Welcome to rawdisk shell. ' \
                     'Type help or ? to list command.\n'
        self.session = Session()
        self.logger = logging.getLogger(__name__)

    def initialize(self):
        self.session.load_plugins()

    def list_plugins(self):
        plugins = self.session.plugin_manager.filesystem_plugins

        data = [
            [plugin.name, plugin.author, plugin.version,
             plugin.description, plugin.plugin_object.identifier_string] for plugin in plugins]

        table = tabulate(
            tabular_data=data,
            headers=['NAME', 'AUTHOR', 'VERSION', 'DESCRIPTION', 'IDENTIFIERS'])

        print(table)

    def do_list(self, resource):
        """
        Enumerate resources
        
        Possible values: plugins
        """
        if resource == 'plugins':
            self.list_plugins()
        else:
            print("Unknown resource: '{}', type 'help list' "
                  "to get more information".format(resource))


    def do_load(self, filename):
        """Load disk image for analysis"""
        try:
            self.session.load(filename)
        except IOError as e:
            self.logger.error(e.strerror)

    def do_session(self, args):
        """Print current session information"""
        pass

    def do_shell(self, command):
        """
        Execute shell command
        
        Use shell [command] or ![command] syntax
        """
        os.system(command)

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
