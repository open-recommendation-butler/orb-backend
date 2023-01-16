

FROM python:3.9.15
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# create the appropriate directories
RUN mkdir -p /home/app

# create the app user
RUN adduser app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

#RUN mkdir /usr/share/elasticsearch

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


# Copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -cR app $HOME
#RUN chown -cR app /usr/share/elasticsearch
#RUN chmod -R a+x /usr/share/elasticsearch
#RUN chmod -R app: /usr/share/elasticsearch

# change to the app user
USER app


# Do migrations
#RUN python manage.py migrate;