#!/bin/sh

/usr/local/bin/uwsgi \
    --http :${UWSGI_PORT} \
    --master \
    --plugin python,http \
    --manage-script-name \
    --mount /=project_amber:app \
    --processes ${UWSGI_PROCESSES} \
    --threads ${UWSGI_THREADS}
