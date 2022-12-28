FROM python:3.8.7-alpine
WORKDIR /usr/src/app
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
#Server will reload itself on file changes if in dev mode
ENV FLASK_ENV=development
COPY requirements.txt requirements.txt
# RUN pip install -U Flask-SQLAlchemy
RUN apk add --update
RUN apk add build-base
RUN apk add libc-dev
RUN apk add libffi-dev
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["flask", "run"]