FROM python:3.6

RUN mkdir -p /usr/src/flask
WORKDIR /usr/src/flask
ADD requirements.txt /usr/src/flask

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

ADD . /usr/src/flask

CMD gunicorn --bind 0.0.0.0:5000 app:app
