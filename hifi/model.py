import hug
import peewee
from datetime import date

# todo: make this a pool in production
database = peewee.SqliteDatabase(':memory:', pragmas=(('foreign_keys', 'on'),))

# first recordings were in the 1850's
first_year_of_recordings = 1850


class PeeweeConnectionMiddleware(object):
    def process_request(self, req, resp):
        database.connect()

    def process_response(self, req, resp, resource):
        if not database.is_closed():
            database.close()


class ApiAlbumYear(hug.types.number):
    """An integer between 1850 and this year"""

    def __call__(self, value):
        value = super().__call__(value)

        if not value > first_year_of_recordings and not value < date.today().year:
            raise ValueError("Enter a year between {} and today", first_year_of_recordings)


class BaseModel(peewee.Model):
    class Meta:
        database = database


class Artist(BaseModel):

    name = peewee.CharField(unique=True)


class Genre(BaseModel):

    name = peewee.CharField(unique=True)


class Album(BaseModel):

    name = peewee.CharField()
    artist = peewee.ForeignKeyField(Artist, related_name='albums', on_delete='CASCADE', on_update='CASCADE')
    genre = peewee.ForeignKeyField(Genre, related_name='albums', on_delete='SET NULL', on_update='CASCADE')
    year = peewee.SmallIntegerField(constraints=[
        peewee.Check('year > {}'.format(first_year_of_recordings)),
        peewee.Check("year < CAST(strftime('%Y', 'now') AS INTEGER)")
    ])

    class Meta:
        indexes = (
            # name and artist must be pair-wise unique
            (('name', 'artist'), True),
        )

    _route = '/albums/{name}/{artist}'

    @classmethod
    @hug.get(_route)
    def get(cls, *args, *kwargs):
        return cls.get()


class Year:
    """Utility for querying albums by year"""

    def __init__(self, year):
        self.year = year

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        assert value <= date.today().year, """Year cannot be in the future"""
        assert value > first_year_of_recordings, """Recordings are not that old"""
        self.__year = value

    @property
    def albums(self):
        """queries albums from this year"""
        raise NotImplementedError


database.create_tables([Artist, Genre, Album], safe=True)
