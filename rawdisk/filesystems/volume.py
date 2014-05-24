import abc


class Volume(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def mount(self, filename, offset):
        """Retrieve volume information."""
        return