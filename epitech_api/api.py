import logging
import requests
from .util import cached_property

class Credentials(object):
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.data = None
        self.cookies = None

    def save_data(self, filename):
        import json

        with open(filename, 'w+') as f:
            json.dump(self.data, f, sort_keys=True, indent=4)

    def save_cookies(self, filename):
        import json

        with open(filename, 'w+') as f:
            json.dump(self.cookies, f, sort_keys=True, indent=4)

    def copy(self):
        credentials = Credentials(self.login, self.password)
        credentials.data = self.data.copy()
        credentials.cookies = self.cookies.copy()
        return credentials

class APIResponse(object):
    def __init__(self, raw):
        self._raw = raw
        self.text = self._raw.text.replace('// Epitech JSON webservice ...\n', '')

    __getattr__ = lambda self, name: getattr(self._raw, name)

    def json(self):
        import json
        return json.loads(self.text)

class EpitechAPI(object):
    BASE_URL = 'https://intra.epitech.eu'

    def __init__(self, login, password):
        self.credentials = Credentials(login, password)
        self.logger = logging.getLogger('EpitechAPI')

    def request(self, path='/', data=None, params=None):
        url = EpitechAPI.BASE_URL + path

        self.logger.debug('REQUEST: %s' % (url))
        params = params if params else {}
        params['format'] = 'json'
        r = requests.post(url, data=data, cookies=self.credentials.cookies, params=params)
        r.raise_for_status()

        return APIResponse(r)

    def login(self):
        data = {
            'login': self.credentials.login,
            'password': self.credentials.password,
            'remind': True,
        }

        try:
            res = self.request(data=data)
            self.credentials.data = res.json()
            self.credentials.cookies = dict(res.cookies)
        except requests.exceptions.HTTPError as e:
            return False

        return True

    @cached_property
    def student(self):
        from .models import Student
        return Student(self, self.credentials.login)

    @cached_property
    def planning(self, **kwargs):
        from .models import Planning
        return Planning(self, **kwargs)

    @staticmethod
    def validate(login, password):
        api = EpitechAPI(login, password)
        return api.login()

    @classmethod
    def from_credentials(credentials):
        api = EpitechAPI(credentials.login, None)
        api.credentials = credentials.copy()
        return api
