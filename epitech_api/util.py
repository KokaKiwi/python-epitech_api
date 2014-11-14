import threading

class cached_property(object):
    def __init__(self, func):
        self.func = func

        self.__doc__ = getattr(self.func, '__doc__')

    def __get__(self, obj, cls):
        if obj is None:
            return self
        if not hasattr(self, 'value'):
            self.value = self.func(obj)
        return self.value

    def __delete__(self, obj):
        if hasattr(self, 'value'):
            del self.value
