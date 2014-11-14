import arrow
from ..models import SimpleModel, create_getter
from collections import OrderedDict
from ..util import cached_property

class NetsoulStat(object):
    def __init__(self, data):
        self.date = arrow.get(data[0])
        self.time_idle = data[2]
        self.timeout_active = data[3]
        self.timeout_idle = data[4]
        self.time_average = data[5]

    def __str__(self):
        return '<NetsoulStat date=%s>' % (self.date)

    def __repr__(self):
        return str(self)

class NetsoulStats(SimpleModel):
    INTRA_PATH = '/user/{login}/netsoul'

    def __init__(self, api, login):
        super().__init__(api)
        self.login = login

    @property
    def req_url(self):
        return NetsoulStats.INTRA_PATH.format(login=self.login)

    @property
    def date_range(self):
        if len(self.data) == 0:
            return None

        first = self.data[0][0]
        last = self.data[-1][0]

        first = arrow.get(first)
        last = arrow.get(last)

        return (first, last)

    @property
    def stats(self):
        return [NetsoulStat(entry) for entry in self.data]

    @property
    def stats_dict(self):
        return OrderedDict([(entry.date, entry) for entry in self.stats])

    def stats_between(self, start, stop):
        if not isinstance(start, arrow.Arrow):
            start = arrow.get(start)
        if not isinstance(stop, arrow.Arrow):
            stop = arrow.get(stop)

        return filter(lambda stat: start <= stat.date <= stop, self.stats)

    def __getitem__(self, timestamp):
        return self.stats_dict[timestamp]
