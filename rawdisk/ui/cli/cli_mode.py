import logging
import os
from rawdisk.session import Session
from tabulate import tabulate
from cmd import Cmd


class CliMode:
    @staticmethod
    def start():
        cli = CliShell()
        cli.initialize()
        cli.cmdloop()


class CliShell(Cmd):
    def __init__(self, session=None):
        super().__init__()
        self.prompt = self.get_prompt()
        self.ruler = '-'
        self.intro = 'Welcome to rawdisk shell. ' \
                     'Type help or ? to list command.\n'

        if session is None:
            self.__session = Session()
        else:
            self.__session = session

        self.logger = logging.getLogger(__name__)

    def initialize(self):
        self.__session.load_plugins()

    def __list_plugins(self):
        plugins = self.__session.filesystem_plugins

        data = [
            [plugin.name, plugin.author, plugin.version, plugin.description,
             plugin.plugin_object.identifier_string] for plugin in plugins]

        table = tabulate(
            tabular_data=data,
            headers=['NAME', 'AUTHOR', 'VERSION', 'DESCRIPTION', 'IDENTIFIERS']
        )

        print(table)

    def __list_volumes(self):
        if self.__session.filename is None:
            self.logger.warning('Please load disk image first')
        else:
            for volume in self.__session.volumes:
                print(volume)

    def do_list(self, resource):
        """
        Enumerate resources

        Possible values: plugins, volumes
        """
        if resource == 'plugins':
            self.__list_plugins()
        elif resource == 'volumes':
            self.__list_volumes()
        else:
            self.logger.error("Unknown resource: '{}', type 'help list' "
                              "to get more information".format(resource))

    def do_load(self, filename):
        """Load disk image for analysis"""
        try:
            self.__session.load(filename)
        except IOError as e:
            self.logger.error(e.strerror)

    def do_session(self, args):
        """Print current session information"""
        filename = 'Not specified' if self.__session.filename is None \
            else self.__session.filename

        print('{0: <30}: {1}'.format('Filename', filename))

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
