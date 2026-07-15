FROM postgres:17-alpine

COPY postgres-local-database/init/01-create-app-database.sh /docker-entrypoint-initdb.d/01-create-app-database.sh
COPY postgres-local-database/init/bootstrap.sql /opt/bootstrap.sql

RUN chmod +x /docker-entrypoint-initdb.d/01-create-app-database.sh

EXPOSE 5432

VOLUME ["/var/lib/postgresql/data"]
