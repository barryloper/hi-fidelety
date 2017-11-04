High Fidelity
=============
The album database

Api Server
----------

install using pip install .

installs script `hifi-api` that starts api server listening on port 8000

open [http://localhost:8000] for documentation

Challenges
----------

CRUD endpoints for albums accessible via POST/GET/UPDATE/DELETE on `/albums/{name}/{artist}`

Index of artists on `/artists`

Endpoint for a particular artists listing their albums on `/artist/{name}`

Endpoint that returns genres ranked by number of albums or lists the years with the most albums on `/counts/{type}` where type is either 'genre' or 'year'

Resources
---------

Albums
name and artist are optional
omit to get a list of matching albums

/v1/albums
GET(query albums), POST(new album)

/v1/albums/{name}/{artist}
GET, PATCH, DELETE

album: {
  'name': 'ziggy stardust',
  'artist': 'david bowie',
  'genre': 'rock',
  'year': 1972,
  'url': '/v1/albums/ziggy stardust/david bowie'

Artists
Artists are created when you create a new album with a non-existent artist

/v1/artists
GET(query artists)

/v1/artists/{name}
GET(get a specific artist)
query params filter albums, or genres

artist: {
  name: david bowie,
  albums: [
    {name: 'ziggy stardust',
     url: '/v1/albums/ziggy stardust/david bowie'
     },
  ]
  }
  
Genres

/v1/genres/{name}
  [{name: 'rock',
    albums: 34}
    ]
    
Years

/v1/years/{year}
  [{year: 1984,
    albums: 33)]
