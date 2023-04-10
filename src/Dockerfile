

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

# Copy project
COPY ./src $APP_HOME

WORKDIR $APP_HOME

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Create database
RUN touch db.sqlite3

# chown all the files to the app user
RUN chown -cR app $HOME

RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('T-Systems-onsite/cross-en-de-roberta-sentence-transformer');"

# change to the app user
USER app