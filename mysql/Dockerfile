FROM mysql:8-oracle

COPY ./dbinit/*.sql /tmp/
COPY ./dbinit/import_db.sh /docker-entrypoint-initdb.d/
COPY ./dbinit/my.cnf /etc/my.cnf

RUN chown mysql:mysql /tmp/*.sql /docker-entrypoint-initdb.d/* /etc/my.cnf

EXPOSE 3306
