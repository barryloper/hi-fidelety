import hug
import falcon
import os
from hifi import db

hug.API(__name__).http.output_format = hug.output_format.pretty_json


@hug.get('/artists')
def get_artists():
    """returns list of artists"""
    return db.get_artists()

@hug.get('/artist/{name}')
def get_artist(name: hug.types.text):
    """ returns list of albums by artist """
    return db.get_artist_albums(name)


@hug.get('/counts', examples='type=genre, type=year')
def get_album_counts(type='genre'):
    """returns genres ranked by number of albums"""
    if type == 'genre':
        return db.get_genres()
    if type == 'year':
        return db.get_years()

@hug.get('/album/{name}/{artist}')
@hug.local()
def get_album(name: hug.types.text,
              artist: hug.types.text,
              response):
    """get an album by name and artist"""
    album = db.get_album(name=name, artist=artist)
    if album is None:
        response.status = falcon.HTTP_404
    else:
        return album


@hug.post('/album/{name}/{artist}')
def create_album(name: hug.types.text,
                 artist: hug.types.text,
                 genre: hug.types.text,
                 year: hug.types.number):
    """create a new album"""
    album_id = db.create_album(name, artist, genre, year)
    return album_id


@hug.put('/album/{name}/{artist}')
def update_album(name: hug.types.text,
                 artist: hug.types.text,
                 new_name: hug.types.text,
                 new_artist: hug.types.text,
                 new_genre: hug.types.text,
                 new_year: hug.types.number,
                 response):
    """update an album.
       must specify the name and artist of a current album.
       must specify all parameters of updated album.
    """
    result = db.update_album(name, artist, new_name, new_artist, new_genre, new_year)

    if result is not 1:
        # update failed. probably because name and artist didn't match an album
        response.status = falcon.HTTP_404


@hug.delete('/album/{name}/{artist}')
def delete_album(name: hug.types.text,
                 artist: hug.types.text,
                 response):
    result = db.delete_album(name, artist)

    if result is not 1:
        # delete failed
        response.status = falcon.HTTP_404


def main():
    hug.API(__name__).http.serve()
