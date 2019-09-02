## Amber Backend

This is the backend app of Project Amber, a task list app.

This is a basic Flask/SQLAlchemy app that takes care of syncing tasks between
devices.

#### Configuration

The config file is a JSON file that is loaded from either `./config.json` or
`/etc/amber.json`, whichever is found first.

Example config:

    {
        "database": "sqlite:///file.db", // SQLAlchemy database URI
        // see https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls
        "allow_signup": false, // whether to allow /api/signup or not
        "loglevel": 0, // 0: errors, 1: warnings, 2: info
        "domain": "https://your.domain.tld" // full domain with HTTPS
        // needed for CORS
    }

If there are environment variables `AMBER_DATABASE` / `AMBER_ALLOW_SIGNUP` /
`AMBER_LOGLEVEL`, `AMBER_DOMAIN` set, the program will respect them and use
over the values provided with the config file.

#### Dependencies

This app directly depends on `flask`, `flask-sqlalchemy`, `flask-cors`, and
`bcrypt`.

#### Running in Docker

The Dockerfile included with the project assumes that:

1. You're going to use either PostgreSQL or SQLite.
2. You're going to run it behind a reverse proxy such as nginx (and running
the app without a reverse proxy won't work because of the current uwsgi
configuration).

If you have to/prefer to use MariaDB, etc, you'll have to add the necessary
Python packages to the Docker image by hand.

#### Licenses

See [LICENSE.txt](LICENSE.txt).
