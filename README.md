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
        "allow_signup": false // whether to allow /api/signup or not
    }

#### Dependencies

This app directly depends on `flask`, `flask-sqlalchemy`, and `bcrypt`.

#### Licenses

See [LICENSE.txt](LICENSE.txt).
