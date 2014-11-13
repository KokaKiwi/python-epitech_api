import logging
from cached_property import cached_property

__all__ = ['student', 'netsoul', 'marks']

# Base classes
class Model(object):
    def __init__(self, api):
        self.api = api

        self.logger = logging.getLogger(self.__class__.__name__)

class SimpleModel(Model):
    def __init__(self, api):
        super().__init__(api)

    def load(self):
        return self.data

    @cached_property
    def data(self):
        res = self.api.request(self.url)
        return res.json()

    get = lambda self, name, default=None: self.data.get(name, default)
    __getitem__ = lambda self, name: self.get(name)

# Util functions
def create_getter(name, default=None, **kwargs):
    def getter(self):
        value = self.get(name)

        if value is None:
            return default

        if 'filter' in kwargs.keys():
            _filter = kwargs['filter']
            value = _filter(value)

        return value
    return property(getter)

def array_map_filter(f):
    def _filter(items):
        return list(map(f, items))
    return _filter

# Imports
from .student import Student
from .netsoul import NetsoulStats
from .marks import Marks
