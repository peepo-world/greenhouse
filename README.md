<!--
SPDX-FileCopyrightText: 2023 peepo.world developers

SPDX-License-Identifier: EUPL-1.2
-->

# greenhouse

The web app behind [peepo.world](https://peepo.world).

To use for development locally:

1) pip install -r /path/to/requirements.txt to install all needed modules

2) Set up postgres db. Don't worry about setting up tables. We'll do this programatically with alembic. I use pgadmin.

3) Make file in /greenhouse/api/db/env.py
    - add variable DATABASE_URL and set string to url for database (ex. postgresql://username:password@localhost/databasename)

4) Once your engine is able to connect to your local db, run command alembic upgrade head to create tables in the database.

5) Create your own application at dev.twitch.tv. At some point we should create one for all of us to connect to...
    - set redirect URL's to http://localhost:8000/authorizecode
    - save client secret to system environment variable TWITCH_CLIENT_SECRET
    - save client id to system environment variable TWITCH_CLIENT_ID

At this point I think you should be able to run the db and web app locally on different ports. There's a decent chance I missed a step or two. 