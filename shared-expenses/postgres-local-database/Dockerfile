FROM postgres:17-alpine

COPY init/01-create-app-database.sh /docker-entrypoint-initdb.d/01-create-app-database.sh

RUN chmod +x /docker-entrypoint-initdb.d/01-create-app-database.sh

EXPOSE 5432

VOLUME ["/var/lib/postgresql/data"]
