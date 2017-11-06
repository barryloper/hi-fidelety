from hifi import model
import logging

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

ozzy, _ = model.Artist.get_or_create(name='Ozzy Osbourne')
metal, _ = model.Genre.get_or_create(name='Metal')

b, _ = model.Album.get_or_create(name='Blizzard Of Ozz', artist=ozzy, genre=metal, year=1980)

print('created album', b)
