# pull official base image
FROM --platform=linux/amd64 python:3.9
# set work directory
WORKDIR /Web Application

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirement.txt .
RUN pip install -r requirement.txt

# copy project
COPY . .