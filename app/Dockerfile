# syntax=docker/dockerfile:1
FROM python:3.9.15
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Do migrations
#RUN python manage.py migrate;