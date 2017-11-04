import hug
import falcon

from .model import AlbumYear


class APIEndpoint:
    """APIEndpoint have access to a DB session.
       don't allow modification of this property
    """

    def __init__(self, db):
        self.__db = db

    @property
    def db(self):
        return self.__db


class Album(APIEndpoint):

    album_route = '/album/{name}/{artist}'

    @hug.get('/counts', examples='type=genre, type=year')
    def get_album_counts(self, type='genre'):
        """returns genres ranked by number of albums"""
        if type == 'genre':
            return self.db.get_genres()
        if type == 'year':
            return self.db.get_years()

    @hug.get(album_route)
    def get_album(self,
                  name: hug.types.text,
                  artist: hug.types.text,
                  response):
        """get an album by name and artist"""
        album = self.db.get_album(name=name, artist=artist)
        if album is None:
            response.status = falcon.HTTP_404
        else:
            return album

    @hug.post(album_route)
    def create_album(self,
                     name: hug.types.text,
                     artist: hug.types.text,
                     genre: hug.types.text,
                     year: AlbumYear):
        """create a new album"""
        album_id = self.db.create_album(name, artist, genre, year)
        return album_id

    @hug.patch(album_route)
    def update_album(self,
                     name: hug.types.text,
                     artist: hug.types.text,
                     new_name: hug.types.text,
                     new_artist: hug.types.text,
                     new_genre: hug.types.text,
                     new_year: hug.types.number,
                     response):
        """update an album.
           must specify the name and artist of a current album.
           must specify all parameters of updated album.
           todo: make all parameters optional
        """
        result = self.db.update_album(name, artist, new_name, new_artist, new_genre,
                                 new_year)

        if result is not 1:
            # update failed. probably because name and artist didn't match an album
            response.status = falcon.HTTP_404

    @hug.delete(album_route)
    def delete_album(self,
                     name: hug.types.text,
                     artist: hug.types.text,
                     response):
        result = self.db.delete_album(name, artist)

        if result is not 1:
            # delete failed
            response.status = falcon.HTTP_404

class Artist(APIEndpoint):
    pass

class Genre(APIEndpoint):
    pass

class Year(APIEndpoint):
    pass
