# -*- coding: utf-8 -*-

from abc import ABCMeta


class Mode(metaclass=ABCMeta):
    @staticmethod
    def entry(args=None):
        """Entry method for utility mode"""