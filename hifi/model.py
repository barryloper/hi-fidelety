import hug
from datetime import date


class AlbumYear(hug.types.number):
    """An integer between 1800 and this year"""

    def __call__(self, value):
        value = super().__call__(value)

        if not value > 1800 and not value < date.today().year:
            raise ValueError("Enter a year between 1800 and today")


class Album:

    def __init__(self, name, artist, genre, year):
        self.name = name
        self.artist = artist
        self.genre = genre
        self.year = year


class ThingWithAlbums:
    def __init__(self, name, *albums):
        self.name = name
        self.albums = albums

    def __str__(self):
        return self.name


class Artist(ThingWithAlbums):
    pass


class Genre(ThingWithAlbums):
    pass


class Year(ThingWithAlbums):
    pass
