from ..models import SimpleModel, create_getter
from cached_property import cached_property

class Student(SimpleModel):
    INTRA_PATH = '/user/{login}'

    PICTURE_URL = 'https://cdn.local.epitech.eu/userprofil/profilview/{login}.jpg'
    MINIATURE_PICTURE_URL = 'https://cdn.local.epitech.eu/userprofil/commentview/{login}.jpg'

    def __init__(self, api, login):
        super().__init__(api)
        self.login = login

    @property
    def url(self):
        return Student.INTRA_PATH.format(login=self.login)

    first_name = create_getter('firstname')
    last_name = create_getter('lastname')

    location = create_getter('location')
    promotion = create_getter('promo')
    promo = promotion

    picture_url = create_getter('picture')

    email = create_getter('internal_email')

    @property
    def miniature_picture_url(self):
        return Student.MINIATURE_PICTURE_URL.format(login=self.login)

    @property
    def gpa_dict(self):
        gpa = self.get('gpa')

        if not gpa:
            return None

        gpa = dict([(o['cycle'], float(o['gpa'])) for o in gpa])
        return gpa

    @property
    def gpa(self):
        values = list(self.gpa_dict.values())
        return values[0]

    year = create_getter('studentyear', filter=int)
    semester = create_getter('semester', filter=int)

    @property
    def groups(self):
        return [o['name'] for o in self.get('groups', [])]

    @cached_property
    def netsoul_stats(self):
        from ..models import NetsoulStats
        return NetsoulStats(self.api, self.login)

    @cached_property
    def marks(self):
        from ..models import Marks
        return Marks(self.api, self.login)

    def __str__(self):
        return '<Student %s %s>' % (self.first_name, self.last_name)

    def __repr__(self):
        return str(self)
