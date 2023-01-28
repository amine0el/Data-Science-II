# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9.16-bullseye

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set DJANGO_DEBUG appropriately
ARG djangodebug
ENV DJANGO_DEBUG ${djangodebug}
RUN echo $DJANGO_DEBUG

# SET REDIS_SERVER appropriately
ARG redisserver
ENV REDIS_SERVER ${redisserver}

# SET postgres values

ARG sqlengine=django.db.backends.sqlite3
ARG sqldatabase=/app/db.sqlite3
ARG sqluser
ARG sqlpassword
ARG sqlhost
ARG sqlport
ARG djangosuperuserusername=admin
ARG djangosuperuserpassword=admin
ARG djangosuperuseremail


ENV SQL_ENGINE ${sqlengine}
ENV SQL_DATABASE ${sqldatabase}
ENV SQL_USER ${sqluser}
ENV SQL_PASSWORD ${sqlpassword}
ENV SQL_HOST ${sqlhost}
ENV SQL_PORT ${sqlport}
ENV TEST_JIRA ${testjira}

# Install pip requirements
COPY requirement.txt .
COPY web_server.txt .
RUN apt-get update
RUN apt-get install libpq-dev libpq5 
RUN apt-get --yes install libsndfile1-dev
RUN apt-get --yes install ffmpeg
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirement.txt -r web_server.txt

WORKDIR /app
COPY . /app

#collect static files
RUN python manage.py collectstatic --noinput


# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "MGC.wsgi", "--timeout 600"]
