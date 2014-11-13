import arrow
from ..models import SimpleModel, create_getter, array_map_filter
from collections import OrderedDict
from cached_property import cached_property

class Mark(object):
    def __init__(self, marks, data):
        self.marks = marks

        self.comment = data['comment']
        self.date = arrow.get(data['date'])
        self.title = data['title']
        self.corrector = data['correcteur']
        self.note = data['final_note']
        self.instance_code = data['codeinstance']
        self.module_code = data['codemodule']
        self.activity_code = data['codeacti']

    @property
    def module(self):
        return self.marks.modules_dict.get(self.module_code)

    def __str__(self):
        return '<Mark code="%s/%s/%s" title=%r note=%r>' % (
            self.instance_code,
            self.module_code,
            self.activity_code,
            self.title,
            self.note,
        )

    __repr__ = str

class Module(object):
    def __init__(self, marks, data):
        self.marks = marks

        self.instance_code = data['codeinstance']
        self.credits = data['credits']
        self.code = data['codemodule']
        self.inscription_date = arrow.get(data['date_ins'])
        self.cycle = data['cycle']
        self.grade = data['grade']
        self.title = data['title']

        # Dunno what this data mean...
        self.raw_barrage = data['barrage']

class Marks(SimpleModel):
    INTRA_PATH = '/user/{login}/notes'

    def __init__(self, api, login):
        super().__init__(api)
        self.login = login

    @property
    def url(self):
        return Marks.INTRA_PATH.format(login=self.login)

    @cached_property
    def marks(self):
        _filter = lambda data: Mark(self, data)
        return map(_filter, self.get('notes'))

    @cached_property
    def modules(self):
        _filter = lambda data: Module(self, data)
        return map(_filter, self.get('modules'))

    @cached_property
    def modules_dict(self):
        return OrderedDict([(module.code, module) for module in self.modules])
