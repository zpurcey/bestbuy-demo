# Use an official Python runtime as a base image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app/bestbuy-demo/

# Make port 80 available to the world outside this container
EXPOSE 80

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_PID_FILE /var/run/apache2/apache2.pid
ENV APACHE_RUN_DIR /var/run/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_LOG_DIR /var/log/apache2

RUN apt-get update \ 
	&& apt-get install -y --no-install-recommends \
		ed \
		less \
		locales \
		vim-tiny \
		wget \
                curl \
		apache2 \
		libapache2-mod-wsgi \
	&& rm -rf /var/lib/apt/lists/*

RUN a2enmod rewrite
RUN a2enmod ssl
RUN a2dissite 000-default

## Configure default locale, see https://github.com/rocker-org/rocker/issues/19
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
	&& locale-gen en_US.utf8 \
	&& /usr/sbin/update-locale LANG=en_US.UTF-8

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8

RUN pip install -r /app/bestbuy-demo/requirements.txt

ADD ./frontend /var/www/frontend
ADD ./backend/__init__.py /var/www/backend/__init__.py

ADD ./backend/bestbuy.conf /etc/apache2/sites-available/bestbuy.conf
ADD ./backend/backend.wsgi /var/www/backend.wsgi 
RUN sed -i.bkp '/<Directory \/var\/www\/>/,/<\/Directory>/ s/Options Indexes FollowSymLinks/Options -Indexes +FollowSymLinks/' /etc/apache2/apache2.conf

RUN a2ensite bestbuy 

RUN chown www-data:www-data /var/www/frontend/static -R
RUN chown www-data:www-data /var/www/frontend/js -R
RUN chown www-data:www-data /var/www/frontend/css -R

RUN export ES_SERVER_IP=$ES_SERVER_IP
RUN export ES_INDEX_NAME=$ES_INDEX_NAME

CMD ["apache2","-DFOREGROUND"]
