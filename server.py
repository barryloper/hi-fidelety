import hug
import os
from hifi.db import initialize_db, DB_LOCATION


def main():
    if not os.path.exists(DB_LOCATION):
        initialize_db()


if __name__ == '__main__':
    main()
