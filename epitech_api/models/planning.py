import arrow
from ..models import SimpleModel, create_getter
from ..util import cached_property

class Event(object):
    URL_PATH = '/module/{year}/{module}/{instance}/{activity}/{event}'

    def __init__(self, api, data):
        self.id = data.get('id')
        self.activity_code = data.get('codeacti')
        self.event_code = data.get('codeevent')
        self.module_code = data.get('codemodule')
        self.instance_code = data.get('codeinstance')
        self.activity_title = data.get('acti_title')
        self.type = data.get('type')
        self.year = data.get('scolaryear')
        self.location = data.get('type')
        self.description = data.get('description')
        self.start = arrow.get(data['start'])
        self.end = arrow.get(data['end'])

        self._fix()

    def _fix(self):
        if self.id is None:
            parts = self.event_code.split('-')
            self.id = int(parts[1])

    @property
    def url_path(self):
        return Event.URL_PATH.format(
            year=self.year,
            module=self.module_code,
            instance=self.instance_code,
            activity=self.activity_code,
            event=self.event_code,
        )

    @property
    def token_url_path(self):
        return self.url_path + '/token'

    @property
    def duration(self):
        return self.end - self.start

class Planning(SimpleModel):
    req_url = '/planning/load'

    def __init__(self, api, start=None, stop=None):
        super().__init__(api)
        self._start = start
        self._stop = stop

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value
        self.reset_data_cache()

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, value):
        self._stop = value
        self.reset_data_cache()

    def select_week(self):
        now = arrow.utcnow()
        (start, stop) = now.span('week')
        self.start = start
        self.stop = stop
        return self

    @property
    def req_params(self):
        params = {}

        if self.start:
            params['start'] = self.start.format('YYYY-MM-DD')
        if self.stop:
            params['stop'] = self.stop.format('YYYY-MM-DD')

        return params

    @property
    def events(self):
        return map(lambda entry: Event(self, entry), self.data)

    def find(self, pred):
        return next(event for event in self.events if pred(event))

    def find_by_id(self, event_id):
        return self.find(lambda event: event.id == event_id)
