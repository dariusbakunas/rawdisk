import unittest
from rawdisk.util.singleton import Singleton

class MockSingleton(metaclass=Singleton):
    def __init__(self):
        self.x = 0x10

class TestSingleton(unittest.TestCase):
    def testReturnsSameInstance(self):
        first = MockSingleton()
        second = MockSingleton()

        self.assertIs(first, second)
