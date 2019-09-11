FROM python:3.7-alpine3.10
MAINTAINER shiwei@baoxian-sz.com

WORKDIR /workspace
COPY . .

RUN pip install -r requirements.txt && \
    chmod +x launch.sh

CMD ./launch.sh
EXPOSE 6001
