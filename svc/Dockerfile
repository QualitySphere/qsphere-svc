FROM python:3.7-alpine3.10
MAINTAINER shiwei@baoxian-sz.com

WORKDIR /workspace
COPY . .

RUN rm -rf mui && \
    apk add --no-cache --update libpq && \
    apk add --no-cache --virtual temp-apks \
        gcc musl-dev python-dev postgresql-dev libffi-dev && \
    pip install -r requirements.txt && \
    apk del temp-apks

CMD ./launch.sh
EXPOSE 6001

HEALTHCHECK --interval=10s --timeout=5s --retries=3 CMD /bin/bash /opt/test.sh
