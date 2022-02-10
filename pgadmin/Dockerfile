FROM dpage/pgadmin4
USER pgadmin
RUN mkdir -p  /var/lib/pgadmin/storage/pgadmin_pgadmin.com
COPY ./pgpass /var/lib/pgadmin/storage/pgadmin_pgadmin.com/
USER root
RUN chown pgadmin:pgadmin /var/lib/pgadmin/storage/pgadmin_pgadmin.com/pgpass
RUN chmod 0600 /var/lib/pgadmin/storage/pgadmin_pgadmin.com/pgpass
USER pgadmin
ENTRYPOINT ["/entrypoint.sh"]