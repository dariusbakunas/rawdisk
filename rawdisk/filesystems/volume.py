import abc


class Volume(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def mount(self, filename, offset):
        """Retrieve volume information."""
        return

    @abc.abstractmethod
    def unmount(self):
        """Close fd when finished"""
        return

    @abc.abstractmethod
    def is_mounted(self):
        """Returns True if fd is not closed"""
        return