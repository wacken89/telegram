FROM wacken/telebot

MAINTAINER Roman Pridybailo <roman.pridybailo@kruschecompany.com>

ADD code /code
COPY docker-entrypoint.sh /usr/local/bin/
WORKDIR /code

ENTRYPOINT ["docker-entrypoint.sh"]