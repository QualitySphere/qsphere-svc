FROM bxwill/qsphere:svc-base
MAINTAINER shiwei@baoxian-sz.com

WORKDIR /workspace
COPY . .

CMD ./launch.sh
EXPOSE 80

HEALTHCHECK --interval=10s --timeout=5s --retries=3 CMD ./health_check.sh
