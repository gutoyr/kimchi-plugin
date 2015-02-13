from backend.exception import InvalidOperation, NotFoundError
from time import sleep


class ResourceSampleModel(object):
    def __init__(self):
        self._state = None

    def lookup(self, params=None):
        return {'state': self._state}

    def update(self, name, params):
        self._state = params['state']

    def start(self, name):
        self._state = 'Step00'

    def delete(self, name):
        self._state = None
