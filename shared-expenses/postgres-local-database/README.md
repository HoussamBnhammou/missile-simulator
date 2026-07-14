# Local PostgreSQL Database

This package runs only PostgreSQL. It contains no Flask or Python container.

## Requirements

- Docker Desktop, or Docker Engine with Docker Compose

## Start the database

```bash
docker compose up -d
```

On Windows, you may double-click `start.bat`.

On macOS or Linux:

```bash
./start.sh
```

Check the container:

```bash
docker compose ps
docker compose logs -f postgres-db
```

Wait until its status reports `healthy`.

## Stop and restart

Stop without deleting the database:

```bash
docker compose stop
```

Start it again:

```bash
docker compose start
```

Remove the container but keep the database data:

```bash
docker compose down
```

Delete the container and all stored database data:

```bash
docker compose down -v
```

> The initialization script runs only when the data volume is empty. If you change
> the database name, user, or passwords after the first startup, run
> `docker compose down -v` before starting again. This deletes existing data.


## Database administration

Oracle SQL Developer is designed primarily for Oracle Database and is not the
recommended PostgreSQL client. Use one of these instead:

- pgAdmin
- DBeaver
- DataGrip
- the `psql` command-line client

### DBeaver or pgAdmin connection

- Host: `localhost`
- Port: `5432`
- Database: `flask_db`
- Username: `flask_app`
- Password: `FlaskDb_12345`

## Open a PostgreSQL terminal inside the container

As the application user:

```bash
docker compose exec postgres-db psql -U flask_app -d flask_db
```

As the administrator:

```bash
docker compose exec postgres-db psql -U postgres -d postgres
```
