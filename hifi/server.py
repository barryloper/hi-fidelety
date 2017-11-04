import hug
import falcon
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



