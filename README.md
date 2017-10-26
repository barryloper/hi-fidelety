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
