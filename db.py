import sqlite3
import csv
import pkg_resources
from pathlib import Path
from functools import partial

__all__ = ['initialize_db', 'get_artists', 'get_album', 'update_album', 'create_album', 'delete_album']

DB_LOCATION = Path.home() / 'hifi.sqlite'

connect = partial(sqlite3.connect, str(DB_LOCATION))


def initialize_db():
    CSV_FILE = pkg_resources.resource_filename('hifi', 'data/albums.csv')
    tables = """
        CREATE TABLE 'artists' (
          artist_id INTEGER PRIMARY KEY,
          name TEXT UNIQUE NOT NULL
        );
        CREATE TABLE 'genres' (
          genre_id INTEGER PRIMARY KEY,
          name TEXT UNIQUE NOT NULL
        );
        CREATE TABLE 'albums' (
          album_id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          year INTEGER NOT NULL,
          artist_id INTEGER NOT NULL,
          genre_id INTEGER NOT NULL,
          UNIQUE (name, artist_id),
          FOREIGN KEY(artist_id) REFERENCES artists(artist_id),
          FOREIGN KEY(genre_id) REFERENCES genres(genre_id)
        );
    """

    with connect() as conn:
        curr = conn.cursor()
        curr.executescript(tables)

    with connect() as conn:
        curr = conn.cursor()
        with open(CSV_FILE, 'r',
                  encoding='cp1252') as f:  # csv has a non-standard encoding
            reader = csv.DictReader(f, dialect='excel')

            for row in reader:
                try:
                    curr.execute("""INSERT INTO artists(name) VALUES (?)""", (row['artist'],))
                    artist_id = curr.lastrowid
                except sqlite3.IntegrityError as e:
                    """ Artist already exists """
                    curr.execute("""SELECT artist_id from artists WHERE name=?""", (row['artist'],))
                    artist = curr.fetchone()
                    artist_id = artist[0]
                try:
                    curr.execute("""INSERT INTO genres(name) VALUES (?)""", (row['genre'],))
                    genre_id = curr.lastrowid
                except sqlite3.IntegrityError as e:
                    """ genre already exists """
                    curr.execute("""SELECT genre_id FROM genres WHERE name=?""", (row['genre'],))
                    genre = curr.fetchone()
                    genre_id = genre[0]

                curr.execute("""INSERT INTO 'albums' (name, artist_id, genre_id, year) VALUES (?, ?, ?, ?)""", (row['album'], artist_id, genre_id, int(row['year'])))


def get_artists():
    with connect() as conn:
        curr = conn.execute("""SELECT name FROM artists""")
        results = curr.fetchall()
    return [{'name': result[0]} for result in results]


def _create_artist(name):
    """ returns database id
        does not create duplicates (case-sensitive)
    """
    with connect() as conn:
        curr = conn.execute("""SELECT artist_id FROM artists WHERE name=?""", (name,))
        existing_artist = curr.fetchone()
        if existing_artist is None:
            curr.execute("""INSERT INTO artists(name) VALUES (?)""", (name,))
            artist_id = curr.lastrowid
        else:
            artist_id = existing_artist[0]

    return artist_id


def _create_genre(name):
    """ returns database id
        does not create duplicates (case-sensitive)
    """
    with connect() as conn:
        curr = conn.execute("""SELECT genre_id FROM genres WHERE name=?""", (name,))
        existing_genre = curr.fetchone()
        if existing_genre is None:
            curr.execute("""INSERT INTO genres(name) VALUES (?)""", (name,))
            genre_id = curr.lastrowid
        else:
            genre_id = existing_genre[0]

    return genre_id


def create_album(name, artist, genre, year):
    """ returns database id if insert is successful """
    artist_id = _create_artist(artist)
    genre_id = _create_genre(genre)
    with connect() as conn:
        curr = conn.execute("""INSERT INTO albums(name, artist_id, genre_id, year) 
                               VALUES (?, ?, ?, ?)""", (name, int(artist_id), int(genre_id), int(year)))
    return curr.lastrowid


def _get_album_row(name, artist):
    with connect() as conn:
        curr = conn.execute(""" SELECT albums.name AS album, 
                                       artists.name AS artist, 
                                       genres.name AS genre, 
                                       albums.year AS year,
                                       album_id,
                                       artist_id,
                                       genre_id
                                FROM albums 
                                JOIN artists USING (artist_id)
                                JOIN genres USING (genre_id)
                                WHERE album=? AND artist=?
                            """, (name, artist))
        result = curr.fetchone()
    return result

def get_album(name, artist):
    """ get a single album by unique name and artist """
    result = _get_album_row(name, artist)

    if result is not None:
        return {'name': result[0],
                'artist': result[1],
                'genre': result[2],
                'year': result[3]}
    else:
        return result


def get_artist_albums(artist):
    """ this will be useful for the "index of artists requirement"
        in an index of artists, each name could link to a list of albums
    """
    raise NotImplementedError


def get_genre_albums(genre):
    raise NotImplementedError


def get_year_albums(year):
    raise NotImplementedError


def update_album(old_name, old_artist, name, artist, genre, year):
    """ should return 1 if successful """
    current_album_row = _get_album_row(old_name, old_artist)
    print(current_album_row)
    with connect() as conn:
        new_artist_id = _create_artist(artist)
        new_genre_id = _create_genre(genre)
        curr = conn.execute("""UPDATE albums 
                               SET name=?,
                                   artist_id=?,
                                   genre_id=?,
                                   year=?
                               WHERE album_id=?
                            """,
                            (name, new_artist_id, new_genre_id, year, current_album_row[4])
                            )

    return curr.rowcount


def delete_album(name, artist):
    """ returns number of deleted rows"""
    with connect() as conn:
        curr = conn.execute("""DELETE FROM albums WHERE name=? AND 
                                  artist_id=(SELECT artist_id FROM artists WHERE name=?)""",
                            (name, artist))
    return curr.rowcount
