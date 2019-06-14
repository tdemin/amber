#!/bin/sh

/usr/local/bin/uwsgi \
    --socket :${UWSGI_PORT} \
    --master \
    --manage-script-name \
    --mount /=project_amber:app \
    --processes ${UWSGI_PROCESSES} \
    --threads ${UWSGI_THREADS}
