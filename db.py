import sqlite3
import sys
import os
import csv
import pkg_resources
from pathlib import Path

DB_LOCATION = Path.home() / 'hifi.sqlite'


def initialize_db():
    CSV_FILE = pkg_resources.resource_filename('hifi', 'data/albums.csv')
    tables = """
        CREATE TABLE 'artists' (
          id INTEGER PRIMARY KEY,
          name TEXT UNIQUE NOT NULL
        );
        CREATE TABLE 'genres' (
          id INTEGER PRIMARY KEY,
          name TEXT UNIQUE NOT NULL
        );
        CREATE TABLE 'albums' (
          id INTEGER PRIMARY KEY,
          name TEXT UNIQUE NOT NULL,
          year INTEGER NOT NULL,
          artist INTEGER NOT NULL,
          genre INTEGER NOT NULL,
          FOREIGN KEY(artist) REFERENCES artists(id),
          FOREIGN KEY(genre) REFERENCES genres(id)
        );
    """

    with sqlite3.connect(str(DB_LOCATION)) as conn:
        curr = conn.cursor()
        curr.executescript(tables)

    with sqlite3.connect(str(DB_LOCATION)) as conn:
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
                    curr.execute("""SELECT id from artists WHERE name=?""", (row['artist'],))
                    artist = curr.fetchone()
                    artist_id = artist[0]
                try:
                    curr.execute("""INSERT INTO genres(name) VALUES (?)""", (row['genre'],))
                    genre_id = curr.lastrowid
                except sqlite3.IntegrityError as e:
                    """ genre already exists """
                    curr.execute("""SELECT id FROM genres WHERE name=?""", (row['genre'],))
                    genre = curr.fetchone()
                    genre_id = genre[0]

                curr.execute("""INSERT INTO 'albums' (name, artist, genre, year) VALUES (?, ?, ?, ?)""", (row['album'], artist_id, genre_id, int(row['year'])))
