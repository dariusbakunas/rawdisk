import abc


class Volume(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def load(self, filename, offset):
        """Load volume information."""
        return