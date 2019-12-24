FROM python:3.7-alpine
LABEL maintainer "Timur Demin <me@tdem.in>"
WORKDIR /app
ENV UWSGI_PORT 8080
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 2

COPY requirements.txt setup.py setup.cfg /app/
COPY bin /app/bin
COPY --chown=0:0 doc/config.json.example /etc/amber.json

# we do not remove postgresql-dev after installation, as psycopg2 needs libpq
# present on the system
RUN adduser -D -u 1000 amber && \
    mkdir -p /data && chown amber /data && chmod 700 /data && \
    apk add --no-cache build-base libffi-dev postgresql-dev && \
    pip install -r requirements.txt && \
    pip install uwsgi psycopg2 && \
    apk del build-base libffi-dev && \
    chmod +x /app/bin/run_uwsgi.sh

COPY project_amber /app/project_amber

USER amber
CMD [ "sh", "/app/bin/run_uwsgi.sh" ]
