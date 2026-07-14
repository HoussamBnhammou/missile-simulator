#!/bin/sh
set -eu

: "${APP_DB:?APP_DB is required}"
: "${APP_USER:?APP_USER is required}"
: "${APP_PASSWORD:?APP_PASSWORD is required}"

psql   --username "$POSTGRES_USER"   --dbname "$POSTGRES_DB"   --set=ON_ERROR_STOP=1   --set=app_db="$APP_DB"   --set=app_user="$APP_USER"   --set=app_password="$APP_PASSWORD" <<'SQL'
SELECT format(
    'CREATE ROLE %I LOGIN PASSWORD %L',
    :'app_user',
    :'app_password'
)
WHERE NOT EXISTS (
    SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = :'app_user'
)
\gexec

SELECT format(
    'CREATE DATABASE %I OWNER %I',
    :'app_db',
    :'app_user'
)
WHERE NOT EXISTS (
    SELECT 1 FROM pg_database WHERE datname = :'app_db'
)
\gexec

SELECT format(
    'GRANT ALL PRIVILEGES ON DATABASE %I TO %I',
    :'app_db',
    :'app_user'
)
\gexec
SQL
