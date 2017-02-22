FROM wacken/db:5.7

COPY docker-entrypoint.sh /usr/local/bin/
RUN mkdir /status && chmod -R 777 /status \
    && chown -R mysql:mysql /docker-entrypoint-initdb.d \
    && rm /entrypoint.sh && ln -s usr/local/bin/docker-entrypoint.sh /entrypoint.sh # backwards compat
ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 3306
CMD ["mysqld"]