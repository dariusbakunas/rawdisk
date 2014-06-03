class Singleton(object):

    __instance__ = None

    def __new__(cls, *a, **kw):
        if Singleton.__instance__ is None:
            Singleton.__instance__ = object.__new__(cls, *a, **kw)
            cls._Singleton__instance = Singleton.__instance__
        return Singleton.__instance__

    def _drop_it(self):
        Singleton.__instance__ = None