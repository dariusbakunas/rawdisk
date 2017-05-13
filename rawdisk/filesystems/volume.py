# -*- coding: utf-8 -*-


import abc


class Volume(object, metaclass=abc.ABCMeta):
    """This is base class for all Volume objects supplied by
    filesystem plugins.
    """

    @abc.abstractmethod
    def load(self, filename, offset):
        """Load volume information.

        Args:
            filename: Filename or device that it will read volume.
            information from.
            offset: Volume offset.
        """
        return

    @abc.abstractmethod
    def dump_volume(self):
        """Print volume information to std output,
        similar to ntfsprogs_1.22 package"""
