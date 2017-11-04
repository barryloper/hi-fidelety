import os
import hug
import argparse
import pkg_resources
from pathlib import Path

from . import db

cli = argparse.ArgumentParser(description="start High Fidelity API Server")
cli.add_argument('-i', '--init', action="store_true", help="""Imports demo data from the package's albums.csv """)


CSV_FILE = pkg_resources.resource_filename('hifi', 'data/albums.csv')

DB_LOCATION = Path.home() / 'hifi.sqlite'


def main():
    db.initialize_db()
    if cli.parse_args('-f'):
        db.import_csv()

    hug.API(__name__).http.serve()
